import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('globalterrorismdb.csv', encoding = 'latin-1', low_memory=True)
df =df[['eventid', 'iyear','imonth', 'iday', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']]

countries = df['country_txt'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in countries],
                value='Brazil'
            ),
            dcc.RadioItems(
                id='dead',
                options=[{'label': i, 'value': i} for i in ['Todos','Com morte', 'Sem morte']],
                value='Todos',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block', 'background': '#000000'}),
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['iyear'].min(),
        max=df['iyear'].max(),
        value=df['iyear'].max(),
        marks={str(year): str(year) for year in df['iyear'].unique()},
        step=None
    )
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('country', 'value'),
     Input('dead', 'value'),
     Input('year--slider', 'value')])
def update_graph(country, dead, year_value):
    dff = df[df['iyear'] == year_value]

    fig = px.scatter_mapbox(dff, 
                        lat='latitude',
                        lon='longitude',
                        text='city',
                        color='iyear',
                        color_continuous_scale=px.colors.cyclical.IceFire,
                        mapbox_style='carto-positron')
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})
    return fig



if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)