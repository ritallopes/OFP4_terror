import plotly.express as px

import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('globalterrorismdb.csv', encoding = 'latin-1', low_memory=True)
df =df[['eventid', 'iyear','imonth', 'iday', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']]
df['iyear']= df['iyear'].astype(int)
countries = np.append(['Todos'], df['country_txt'].sort_values().unique())

def scatter_attacks(dataframe):
    paises = pd.DataFrame(dataframe.country_txt.value_counts())
    paises.columns = ['n_attacks']
    most_attacked = paises.loc[paises.n_attacks >100]
    fig = px.scatter(most_attacked,
                    y= 'n_attacks',
                    x=most_attacked.index,
                    color='n_attacks',
                    marginal_y = 'histogram',
                    template='plotly_white')
    return fig


app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in countries],
                value='Todos'
            ),
            dcc.RadioItems(
                id='dead',
                options=[{'label': i, 'value': i} for i in ['Todos','Com morte', 'Sem morte']],
                value='Todos',
                labelStyle={'display': 'inline-block', 'color': '#ffffff'}
            )
        ],
        style={'width': '10%', 'height': '100vh','min-height': '100%','display': 'inline-block', 'background': '#000000', 'margin':'0'}),
   
    html.Div([
           dcc.Graph(id='indicator-graphic'),
           dcc.Graph(id='scatter-attacks', figure= scatter_attacks(df))
        ],
        style={'width': '88%', 'height': '50vh','display': 'inline-block', 'float':'right',  'margin':'0'}),
    ])  
], style={'width': '100%', 'height': '50vh'})

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('country', 'value'),
     Input('dead', 'value')])
def update_graph(country, dead):
    dff = df
    z = 1
    if(country !="Todos"):
      dff = df.loc[df['country_txt'] == country].copy()
      z=3
    
    if(dead =="Com morte"):
      dff = dff.loc[dff['nkill'] >0].copy()
    elif(dead =="Sem morte"):
      dff = dff.loc[dff['nkill'] == 0].copy()
    
    fig = px.scatter_mapbox(dff, 
                        lat='latitude',
                        lon='longitude',
                        text='city',
                        color='iyear',
                        zoom= z,
                        color_discrete_sequence=px.colors.qualitative.G10,
                        mapbox_style='carto-positron')    
    fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

    return fig
if __name__ == '__main__':
    app.run_server(debug=True)