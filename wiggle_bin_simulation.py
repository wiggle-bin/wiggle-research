import xarray as xr
import pandas as pd

def simulate(df, 
             color='black', 
             insulation=False, 
             in_shade=False, 
             partial_shade=False, 
             sunlight_hours=(10, 15), 
             use_soil_as_ambient=False,
             soil_column='soil_0_7',
             include_compost_heat=False,
             compost_heat_rate=5,
             solar_heating_panel=False,
             solar_panel_area=0.15,  # NEW PARAMETER: area in m²
             fan_active=False,
             include_ice_packs=False,
             auto_venting_lid=False,
             smart_venting_lid=False,
             pcm_mass_kg=0,
             pcm_latent_heat=334000,
             shade_on_hot_days=False):

    # Constants
    heat_capacity_bin = 1e5 if insulation else 5e4
    emissivity = 0.95
    sigma = 5.67e-8
    absorptivity = 0.9 if color == 'black' else 0.3

    dt = 3600  # seconds per time step (1 hour)
    surface_area = 0.5  # m² (bin surface area)

    # Initial temperature
    T = df[soil_column].iloc[0] if use_soil_as_ambient else df['temp'].iloc[0]
    temperatures = []
    pcm_latent_used = 0
    pcm_temp = T

    # Precompute daily max temperatures for hot-day shading
    if shade_on_hot_days:
        daily_max_temp = df['temp'].groupby(df.index.date).max()

    for i in range(len(df)):
        timestamp = df.index[i]
        ambient = df[soil_column].iloc[i] if use_soil_as_ambient else df['temp'].iloc[i]
        sun = df['sun'].iloc[i]
        hour = timestamp.hour
        current_date = timestamp.date()

        # Determine if bin should be in shade due to high daily temp
        if shade_on_hot_days and daily_max_temp[current_date] > 30:
            effective_shade = True
        else:
            effective_shade = in_shade

        if effective_shade:
            sun *= 0.1
        elif partial_shade and not (sunlight_hours[0] <= hour < sunlight_hours[1]):
            sun *= 0.1

        # Heat contributions
        solar_fraction = 0.2 if use_soil_as_ambient else 1.0
        solar_energy = absorptivity * sun * surface_area * dt * solar_fraction
        compost_energy = compost_heat_rate * dt if include_compost_heat else 0

        # Solar heating panel contribution
        panel_efficiency = 0.6
        solar_panel_power = solar_panel_area * sun * panel_efficiency
        panel_solar_fraction = 0.2 if use_soil_as_ambient else 1.0
        solar_panel_energy = solar_panel_power * dt * panel_solar_fraction if solar_heating_panel else 0

        # Heat losses
        conv_coeff = 1.5 if (use_soil_as_ambient and insulation) else \
                     3.0 if use_soil_as_ambient else \
                     2.0 if insulation else 5.0
        conv_energy_loss = conv_coeff * surface_area * (T - ambient) * dt

        rad_emissivity = emissivity * 0.5 if use_soil_as_ambient else emissivity
        T_K = T + 273.15
        ambient_K = ambient + 273.15
        rad_energy_loss = rad_emissivity * sigma * surface_area * (T_K**4 - ambient_K**4) * dt

        # Venting
        vent_energy_loss = 0
        if smart_venting_lid:
            if hour in range(0, 7) or hour in range(19, 24):
                if T > ambient:
                    vent_energy_loss = 30 * surface_area * (T - ambient) * dt
        elif auto_venting_lid and T > 30:
            vent_coeff = 20 if not use_soil_as_ambient else 10
            vent_energy_loss = vent_coeff * surface_area * (T - ambient) * dt

        # Fan cooling
        fan_energy_loss = 0
        if fan_active and T > 30:
            fan_energy_loss = 40 * surface_area * (T - ambient) * dt

        # Ice packs
        ice_pack_energy_loss = 0
        if include_ice_packs and 12 <= hour <= 17 and T > 30:
            ice_pack_energy_loss = 200 * surface_area * (T - ambient) * dt

        # PCM buffering
        pcm_energy_change = 0
        if pcm_mass_kg > 0:
            if T < pcm_temp and pcm_latent_used < pcm_mass_kg * pcm_latent_heat:
                latent_capacity_left = pcm_mass_kg * pcm_latent_heat - pcm_latent_used
                energy_to_absorb = min(latent_capacity_left, heat_capacity_bin * (pcm_temp - T))
                pcm_energy_change = energy_to_absorb
                pcm_latent_used += energy_to_absorb
            elif T > pcm_temp and pcm_latent_used > 0:
                energy_to_release = min(pcm_latent_used, heat_capacity_bin * (T - pcm_temp))
                pcm_energy_change = -energy_to_release
                pcm_latent_used -= energy_to_release
            T += pcm_energy_change / heat_capacity_bin

        # Net energy
        net_energy = solar_energy + compost_energy + solar_panel_energy \
                     - conv_energy_loss - rad_energy_loss \
                     - vent_energy_loss - fan_energy_loss - ice_pack_energy_loss

        T += net_energy / heat_capacity_bin
        temperatures.append(T)

    return temperatures


def load_and_process_emwcf_data(temp_path, rad_path):
    """
    Load and process EMWCF weather data (temperature + radiation).

    Args:
        temp_path (str): Path to NetCDF file with temperature data.
        rad_path (str): Path to NetCDF file with radiation data.

    Returns:
        pd.DataFrame: Combined and processed DataFrame with:
            - 'temp' in °C
            - 'soil_0_7' in °C
            - 'sun' in W/m²
            - 'month' column (int)
            - Datetime index named 'time'
    """
    # Load datasets
    temp_ds = xr.open_dataset(temp_path)
    rad_ds = xr.open_dataset(rad_path)

    # Merge and convert to DataFrame
    combined = xr.merge([temp_ds, rad_ds])
    df = combined.to_dataframe().reset_index()

    # Convert units
    df['temp'] = df['t2m'] - 273.15           # K → °C
    df['soil_0_7'] = df['stl1'] - 273.15      # K → °C
    df['sun'] = df['ssrd'] / 3600             # J/m² per 2h → W/m²

    # Rename and process datetime
    df = df.rename(columns={"valid_time": "time"})
    df['month'] = pd.to_datetime(df['time']).dt.month
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index)

    return df

def add_bin_models_air_soil(df, base_models):
    """
    For each base model, create two simulation columns:
    - air variant (as is)
    - soil variant (with use_soil_as_ambient=True added)

    Columns are named like: "{model_name}_air" and "{model_name}_soil".

    Args:
        df (pd.DataFrame): Input DataFrame
        base_models (dict): keys are model names (e.g. 'model_A'),
                            values are param dicts for simulate()

    Returns:
        pd.DataFrame: df with new simulation columns added.
    """
    for model_name, params in base_models.items():
        # Air variant
        air_col = f"{model_name}_air"
        df[air_col] = simulate(df, **params)

        # Soil variant: add 'use_soil_as_ambient' param without modifying original dict
        soil_params = params.copy()
        soil_params['use_soil_as_ambient'] = True
        soil_col = f"{model_name}_soil"
        df[soil_col] = simulate(df, **soil_params)

    return df
