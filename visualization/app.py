from influxdb import InfluxDBClient
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

client = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='routing_compliance')

json_data = [
    {
        "measurement": "routingCompliance",
        "tags": {
            "prefix": "192.168.0.0/24",
            "source": "10.200.49.9",
            "as_path": ""
        },
        "time": datetime.now(),
        "fields": {
                "as_origin_compliance": 0,
                "community_compliance": 1,
                "weight_compliance": 0,
                "med_compliance": 0,
        }
    }
]

client.create_database('routing_compliance')
client.write_points(json_data)

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# # assume you have a "long-form" data frame
# # see https://plotly.com/python/px-arguments/ for more options
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })

# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

# app.layout = html.Div(children=[
#     html.H1(children='BGP Routing Compliance Dashbboard'),

#     html.Div(children='''
#         NANOG 80 Hackathon.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)
