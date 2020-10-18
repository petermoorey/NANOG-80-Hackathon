from influxdb import InfluxDBClient
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

client = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='telegraf')
q = 'SELECT * from routingCompliance'
df = pd.DataFrame(client.query(q, chunked=True, chunk_size=10000).get_points())

# routers = [{'label': 'All', 'value': '*'}]
# for v in df.source.unique():
#     routers.append({'label': v, 'value': v})

prefixes = [{'label': 'All', 'value': '*'}]
for v in df.prefix.unique():
    prefixes.append({'label': v, 'value': v})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
fig_origin_compliance = px.area(df, x="time", y="origin_compliance", color="prefix")
fig_as_path_compliance = px.area(df, x="time", y="as_path_compliance", color="prefix")

app.layout = html.Div(children=[
    html.H1(children='BGP Routing Compliance Dashboard'),

    html.H3(children='''NANOG 80 Hackathon'''),

    html.Div([
        # html.Label('Select a router'),
        # dcc.Dropdown(
        #     options=routers,
        #     value='All',
        #     multi=True
        # ),
        html.Label('Select a prefix'),
        dcc.Dropdown(
            options=prefixes,
            value='All',
            multi=True
        )
    ], style={'columnCount': 2}),

    html.Div([
            html.Div([
                    html.H4('Origin - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_origin_compliance',
                        figure=fig_origin_compliance
                    )
                ]
            ),
            html.Div([
                    html.H4('AS Path Compliance - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_as_path_compliance',
                        figure=fig_as_path_compliance
                    )
                ]
            )
        ], style={'columnCount': 2})
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
