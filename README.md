## Worm environment info

| Temperature (°C) | Worm Activity/Health                                                                       |
| ---------------- | ------------------------------------------------------------------------------------------ |
| **< 10**         | Dangerous cold (can die)                                                                   |
| **10–15**        | Low activity                                                                               |
| **15–25**        | Optimal range (peak composting productivity)                                               |
| **25–30**        | **Still productive**, but may start to slow or stress slightly — not necessarily "low" yet |
| **> 30**         | Increasing risk of stress/death, especially >35°C                                          |

| Temperature | Impact                                                                                    |
| ----------- | ----------------------------------------------------------------------------------------- |
| **> 35°C**  | **Lethal zone**: Risk of death due to overheating, protein denaturation, oxygen shortage. |
| **30–35°C** | Stressful, reduced activity, possible heat stress.                                        |
| **15–30°C** | ✅ **Optimal range**: Reproduction and composting most active.                             |
| **5–15°C**  | Slower metabolism, but survivable.                                                        |
| **0–5°C**   | Survival possible but with minimal activity. Risk increases with duration.                |
| **< 0°C**   | ❄️ **Danger zone**: Worms usually die unless deeply insulated or burrowed.                |


| Temperature | Productivity      | Explanation                                                                                                                            |
| ----------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **15°C**    | 🐌 Low            | Worms slow down significantly. They eat and reproduce less. Composting is slow but safe.                                               |
| **25°C**    | ✅ Optimal         | Excellent balance of worm activity, decomposition speed, and microbial action.                                                         |
| **30°C**    | ⚠️ High but risky | Peak productivity, but close to the upper stress limit. Worms may become less active or stressed if it gets warmer. Monitor carefully. |

## Data info

| Column name | ERA5 variable                       | Description                                                                                 | Units  | Depth (if applicable) |
| ----------- | ----------------------------------- | ------------------------------------------------------------------------------------------- | ------ | --------------------- |
| `t2m`       | `2m_temperature`                    | Air temperature at 2 meters above the surface.                                              | Kelvin | —                     |
| `ssrd`      | `surface_solar_radiation_downwards` | Solar energy reaching the surface per unit area (a measure of sun exposure).                | J/m²   | —                     |
| `stl1`      | `soil_temperature_level_1`          | Soil temperature at layer 1                                                                 | Kelvin | **0–7 cm**            |
| `stl2`      | `soil_temperature_level_2`          | Soil temperature at layer 2                                                                 | Kelvin | **7–28 cm**           |
| `stl3`      | `soil_temperature_level_3`          | Soil temperature at layer 3                                                                 | Kelvin | **28–100 cm**         |
| `soil_type` | `soil_type`                         | Categorical code for soil type (e.g., sand, loam, clay) — not typically used for temp plots | —      | —                     |