import yaml

from netaddr import IPNetwork, IPAddress
from influxdb import InfluxDBClient

class ComplianceParser(object):
    def __init__(self, policy: str):
        try:
            with open(policy, 'r') as policy_file:
                policy_def = yaml.load(policy_file, Loader=yaml.FullLoader)
                print(policy_def)
                self.regions = policy_def['regions']
                self.policies = policy_def['policy']
        except KeyError:
            print("Malformed policy.")
            self.regions = []
            self.policies = []
        
        try:
            with open('influx.yml', 'r') as db_context:
                db_params = yaml.load(db_context, Loader=yaml.FullLoader)
                self.db = InfluxDBClient(**db_params)
        except Exception as e:
            print(e)


    def is_in_policy(self, prefix: str) -> str:
        try:
            target_network = IPNetwork(prefix)

            for prefix, policy in self.policies.items():
                parent_network = IPNetwork(prefix)
                
                if policy['match'] == 'any':
                    if prefix in parent_network:
                        return str(parent_network)
                elif policy['match'] == 'explicit':
                        if prefix == parent_network:
                            return prefix
                else:
                    raise NotImplementedError
        except KeyError:
            print("Malformed Policy")
            
        return None

    def evaluate(self, update: dict) -> bool:
        pass
