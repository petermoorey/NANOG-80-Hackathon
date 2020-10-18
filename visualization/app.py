from influxdb import InfluxDBClient
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

client = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='routing_compliance')
q = 'SELECT * from routingCompliance'
df = pd.DataFrame(client.query(q, chunked=True, chunk_size=10000).get_points())

routers = [{'label': 'All', 'value': '*'}]
for v in df.source.unique():
    routers.append({'label': v, 'value': v})

prefixes = [{'label': 'All', 'value': '*'}]
for v in df.prefix.unique():
    prefixes.append({'label': v, 'value': v})

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
fig_community_compliance = px.area(df, x="time", y="community_compliance", color="prefix")
fig_as_origin_compliance = px.area(df, x="time", y="as_origin_compliance", color="prefix")
fig_weight_compliance = px.area(df, x="time", y="weight_compliance", color="prefix")
fig_med_compliance = px.area(df, x="time", y="med_compliance", color="prefix")

app.layout = html.Div(children=[
    html.H1(children='BGP Routing Compliance Dashboard'),

    html.H3(children='''NANOG 80 Hackathon'''),

    html.Div([
        html.Label('Select a router'),
        dcc.Dropdown(
            options=routers,
            value='All',
            multi=True
        ),
        html.Label('Select a prefix'),
        dcc.Dropdown(
            options=prefixes,
            value='All',
            multi=True
        )
    ], style={'columnCount': 2}),

    html.Div([
            html.Div([
                    html.H4('Community Value - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_community_compliance',
                        figure=fig_community_compliance
                    )
                ]
            ),
            html.Div([
                    html.H4('AS Origin Compliance - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_as_origin_compliance',
                        figure=fig_as_origin_compliance
                    )
                ]
            ),
            html.Div([
                    html.H4('Weight Compliance - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_weight_compliance',
                        figure=fig_weight_compliance
                    )
                ]
            ),
            html.Div([
                    html.H4('MED Compliance - Count of Non-Compliant Events'),
                    dcc.Graph(
                        id='fig_med_compliance',
                        figure=fig_med_compliance
                    )
                ]
            )
        ], style={'columnCount': 2})
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
