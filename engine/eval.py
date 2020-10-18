

class ComplianceParser(object):
    def __init__(self, policy: str):
        self.policy = policy

    def __is_in_policy(self, prefix: str) -> bool:
        try:
            target_network = IPNetwork(prefix)

            for prefix, policy in self.policy['policy'].items():
                parent_network = IPNetwork(prefix)
                
                if policy['match'] == 'any':
                    if child_network in parent_network:
                        return True
                elif policy['match'] == 'explicit':
                        if prefix == parent_network:
                            return True
                else:
                    raise NotImplementedError
        except KeyError:
            pass
            
        return False