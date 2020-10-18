from influxdb import InfluxDBClient
from datetime import datetime
import time
import random

client = InfluxDBClient(host='influxdb', port=8086, username='root', password='root', database='routing_compliance')

while True:
    time.sleep(5)
    prefix_third_octet = random.randint(0, 4)
    source_fourth_octet = random.randint(0, 5)

    json_data = [
        {
            "measurement": "routingCompliance",
            "tags": {
                "prefix": f"192.168.{prefix_third_octet}.0/24",
                "source": f"10.200.{source_fourth_octet}.9",
                "as_path": ""
            },
            "time": datetime.now(),
            "fields": {
                    "as_origin_compliance": random.randint(0, 4),
                    "community_compliance": random.randint(0, 4),
                    "weight_compliance": random.randint(0, 4),
                    "med_compliance": random.randint(0, 4),
            }
        }
    ]

    print(json_data)
    client.create_database('routing_compliance')
    client.write_points(json_data)
