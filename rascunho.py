import pandas as pd
import numpy as np
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df_origin = pd.read_csv('globalterrorismdb.csv', encoding ='latin-1', low_memory=False)
df_origin = df_origin[['eventid', 'iyear','imonth', 'iday', 'country_txt', 'region_txt', 'city', 'latitude', 'longitude', 'nkill']]
dataframe_current = df_origin

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

def generate_map(lon, lat):
	return lon+lat
def hist_country(dataframe):
	fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

app.layout = html.Div([
    html.H2('TERRORISMO'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in np.append(['Todos'], df_origin.country_txt.sort_values(ascending=True).unique())],
        value='Todos'
    ),
     dcc.RadioItems(
     	id='radio',
        options=[
            {'label': 'Todos', 'value': 'all'},
            {'label': u'Com mortes', 'value': 'dead'},
            {'label': 'Sem mortes', 'value': 'notdead'}
        ],
        value='all'
    ),
    html.Div(id='display-value'),
    html.Div(id='display-radio')

])
@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
	global dataframe_current
	dataframe_current = df_origin
	if(value != 'Todos'):
		dataframe_current = dataframe_current.loc[ dataframe_current.country_txt == value]
	return generate_table(dataframe_current)

@app.callback(
    dash.dependencies.Output('display-radio', 'children'),
    [dash.dependencies.Input('radio', 'value')])
def radio_value(value):
	global dataframe_current
	dataframe_current = df_origin
    
	return generate_table(dataframe_current.loc[dataframe_current.nkill != 0])

    
if __name__ == '__main__':
    app.run_server(debug=True)