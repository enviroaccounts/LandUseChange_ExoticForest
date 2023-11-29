from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go

def load_forest_land_use_data():
    """Loads forest land use change data."""
    return pd.read_csv("static/data/LandUseChange_ExoticForest_2008_2018.csv")

def prepare_forest_land_use_chart_data(data_df):
    """Prepares data for the forest land use pie chart."""
    # Extract data starting from the 'Producing Grassland' column
    land_use_data = data_df.iloc[0, 3:]
    labels = land_use_data.index.tolist()
    values = land_use_data.values.tolist()
    return labels, values

def create_forest_land_use_pie_chart(labels, values):
    """Creates a pie chart for forest land use data."""
    
    # Calculate percentages and create custom text labels
    total = sum(values)
    percents = [(v / total * 100) for v in values]
    custom_text = [f"<1%" if 0 < p < 1 else f"{p:.0f}%" for p in percents]

    pie_chart = go.Pie(
        labels=labels,
        values=values,
        textinfo='label+percent',
        hoverinfo='label+percent',
        hovertemplate='<b>%{label}</b><br>%{percent:.0%}<br>Total: %{value}<extra></extra>',
        texttemplate=custom_text  # Use custom text labels
    )

    fig = go.Figure(data=[pie_chart])
    fig.update_layout(
        title={
            'text': "Land uses converted into exotic forest between 2008 and 2018.",
            'y': 0.08,  # Adjust the vertical position
            'x': 0.5,  # Center the title horizontally
            'xanchor': 'center',
            'yanchor': 'bottom'
        }
    )

    return fig

def setup_dash_layout(app, fig_pie_chart):
    """Sets up the layout of the Dash app."""
    app.layout = html.Div(children=[
        html.Div([
            dcc.Graph(id='forest-land-use-pie-chart', figure=fig_pie_chart)
        ])
    ], id='forest-land-use-pie-chart-layout')

def create_app():
    """Creates and configures the Dash app."""
    app = Dash(__name__)

    # Load and prepare data
    data_df = load_forest_land_use_data()
    labels, values = prepare_forest_land_use_chart_data(data_df)

    # Create pie chart
    fig_pie_chart = create_forest_land_use_pie_chart(labels, values)

    # Setup layout
    setup_dash_layout(app, fig_pie_chart)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True, host='0.0.0.0', port=8050)
