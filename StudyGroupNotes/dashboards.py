#####################################################
### Creating Dashboards with Python - Plotly Dash ###
#####################################################

# Import libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# Load data at the start of the file.
df = pd.read_csv('weight-height.csv')

# Create an app.
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = 'My App'

# Setup a simple html `div`.
my_heading = html.H1('This is an <h1> text!')

# Creating a graph.
graph = dcc.Graph(id='graph')

# Creating a dropdown.
menu_items = [
    dict(label='Height', value='Height'),
    dict(label='Weight', value='Weight')
]
dropdown_menu = dcc.Dropdown(
    id='dropdown',
    options=menu_items,
    value=None
)

# Creating a Graph / Dropdown Div
graph_div = html.Div(
    children=[graph, dropdown_menu],
    style={
        'margin-top': '100px',
        'margin-bottom': '100px',
        'margin-right': '15%',
        'margin-left': '15%'
    }
)

# Set the layout of the app.
app.layout = html.Div(
    id='main_div',
    children=[my_heading, graph_div],
    style={'width': '90%', 'margin': 'auto', 'padding': '30px'}
)

# Callback
@app.callback(Output('graph', 'figure'), Input('dropdown', 'value'))
def update_figure(string):
    """
    Input: string from dropdown which updates
        the paramaters of the graph.
    Output: graph_object.
    """

    # By default, the `Input` is None.
    if not string:
        raise PreventUpdate

    traces = []
    traces.append(
        go.Histogram(x=df[string][df.Gender=='Male'], name='Male')
        )
    traces.append(
        go.Histogram(x=df[string][df.Gender=='Female'], name='Female')
        )

    return dict(
        data=traces,
        layout=go.Layout(
            title=f'{string} Distribution')
    )

# Run the app.
if __name__ == '__main__':
    app.run_server(debug=True)
