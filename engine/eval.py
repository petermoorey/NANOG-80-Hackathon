import sys
import yaml
import re
import time 

from netaddr import IPNetwork, IPAddress
from influxdb import InfluxDBClient
from datetime import datetime

class ComplianceParser(object):
    def __init__(self, policy: str):
        try:
            with open(policy, 'r') as policy_file:
                policy_def = yaml.load(policy_file, Loader=yaml.FullLoader)
                print(policy_def)
                self.regions = policy_def['regions']
                self.policies = policy_def['policy']
                self.root_path = policy_def['root_path']
                self.source = policy_def['root_source']
        except KeyError:
            print("Malformed policy.")
            self.regions = []
            self.policies = []
        
        try:
            with open('influx.yml', 'r') as db_context:
                db_params = yaml.load(db_context, Loader=yaml.FullLoader)
                self.db = InfluxDBClient(host='163.185.202.37', username='root', password='root', database='telegraf')
        except Exception as e:
            print(e)


    def is_in_policy(self, prefix: str) -> str:
        try:
            target_network = IPNetwork(prefix)

            for prefix, policy in self.policies.items():
                parent_network = IPNetwork(prefix)
                
                if policy['match'] == 'any':
                    if target_network in parent_network:
                        print(f"{target_network} in {parent_network}")
                        return str(parent_network)
                elif policy['match'] == 'explicit':
                        if target_network == parent_network:
                            print(f"{target_network} is {parent_network}")
                            return prefix
                else:
                    raise NotImplementedError
        except KeyError:
            print("Malformed Policy")
            
        return None

    def evaluate(self) -> bool:
        query = f'SELECT * FROM "{self.source}" WHERE time > now() - 15s'
        print(query)
        results = self.db.query(query)
        for result in results.get_points(self.source):
            prefix_path = 'bgp_route_af/bgp_route_filter/bgp_route_entry/prefix'
            prefix = result[prefix_path]
            print(f"Prefix is {prefix} on source {result['source']}")

            if prefix:
                compliance = {}
                policy_prefix = self.is_in_policy(prefix)
                print(f"Policy prefix: {policy_prefix}")
                print(f"evaluating prefix {prefix} in policy")
                if policy_prefix:
                    policy = self.policies[policy_prefix]

                    for key, value in policy['attributes'].items():
                        for attr in result:
                            if 'bgp_neighbor' not in attr:
                                if re.search(f"/{key}$", attr):
                                    if result[attr] == value:
                                        compliance[f"{key}_compliance"] = 0
                                        print(f"prefix {prefix} attribute {key} is {result[attr]} which is compliant based on {value} from source {result['source']}")
                                    else:
                                        compliance[f"{key}_compliance"] = 1
                                        print(f"prefix {prefix} attribute {key} is {result[attr]} which is non-compliant based on {value} from source {result['source']}")
            
                payload = [{
                    "measurement": "routingCompliance",
                    "tags": {
                        "prefix": prefix,
                    },
                    "time": datetime.now(),
                    "fields": compliance
                }]
                print("Comitting to DB")
                print(payload)
                self.db.write_points(payload)
            else:
                print(result)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python eval.py <policy_file> <interval>")
        sys.exit(1)

    parser = ComplianceParser(sys.argv[1])
    while True:
        # Get dataset
        parser.evaluate()

        try:
            time.sleep(int(sys.argv[2]))
        except TypeError:
            print("Interval must be a number")
