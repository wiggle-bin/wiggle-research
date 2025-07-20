import plotly.graph_objects as go

def plot_worm_temperature_zones(df, cols_to_plot, title="Worm Temperature Zones", height=450):
    """
    Plot temperature data with shaded worm temperature zones using Plotly.

    Args:
        df (pd.DataFrame): DataFrame with datetime index.
        cols_to_plot (dict): Dict of column names to plot and their display properties, e.g.:
            {
                'bin_black_model_air': {'name': 'WiggleBin (black box)', 'color': 'purple'},
                'bin_white_model_air': {'name': 'WiggleBin (white box)', 'color': 'orange'}
            }
        title (str): Plot title.
        height (int): Height of the plot.

    Returns:
        plotly.graph_objects.Figure: The Plotly figure object.
    """

    zone_colors = [
        {'y0': -5, 'y1': 10, 'color': 'blue', 'label': 'Dangerous Cold'},
        {'y0': 10, 'y1': 15, 'color': 'lightblue', 'label': 'Low Productivity'},
        {'y0': 15, 'y1': 25, 'color': 'green', 'label': 'Peak Productivity'},
        {'y0': 25, 'y1': 30, 'color': 'orange', 'label': 'Low Productivity'},
        {'y0': 30, 'y1': 50, 'color': 'red', 'label': 'Dangerous Heat'}
    ]

    fig = go.Figure()

    # Add shaded zones
    for zone in zone_colors:
        fig.add_shape(
            type="rect",
            x0=df.index[0], x1=df.index[-1],
            y0=zone['y0'], y1=zone['y1'],
            fillcolor=zone['color'],
            opacity=0.1,
            layer="below",
            line_width=0
        )

    # Add traces for each column
    for col, props in cols_to_plot.items():
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df[col],
            mode='lines',
            name=props.get('name', col),
            # line=dict(color=props.get('color', 'black'), width=2),
            opacity=0.7
        ))

    # Update layout
    fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        template="plotly_white",
        height=height,
        legend=dict(x=0.01, y=0.99)
    )

    return fig

import pandas as pd
import plotly.express as px

zone_bins = [-float('inf'), 0, 10, 15, 30, 35, float('inf')]
zone_labels = [
    'Freezing (<0°C)',
    'Cold (0–10°C)',
    'Suboptimal (10–15°C)',
    'Productive (15–30°C)',
    'Stress (30–35°C)',
    'Melting (>35°C)'
]

def plot_hours_in_temperature_zones(series_dict, title="Time Spent in Worm Temperature Zones"):
    """
    Given a dict of {label: pd.Series}, classify each series into temperature zones,
    count hours in each zone, combine, and plot grouped bar chart.

    Args:
        series_dict (dict): keys are model names/labels, values are pd.Series of temperatures
        title (str): Plot title

    Returns:
        plotly.graph_objs.Figure: The Plotly figure object.
    """
    dfs = []
    for label, series in series_dict.items():
        categories = pd.cut(series, bins=zone_bins, labels=zone_labels, right=False)
        counts = categories.value_counts().sort_index()
        df = pd.DataFrame({'Zone': counts.index, 'Hours': counts.values, 'Model': label})
        dfs.append(df)

    zone_df = pd.concat(dfs)

    fig = px.bar(
        zone_df,
        x='Zone',
        y='Hours',
        color='Model',
        barmode='group',
        title=title,
        category_orders={'Zone': zone_labels}
    )

    fig.update_layout(
        xaxis_title='Soil Temperature',
        yaxis_title='Number of Hours',
        xaxis=dict(tickangle=0),
    )

    return fig
