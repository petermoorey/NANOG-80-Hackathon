import sys
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
from ncclient import manager


INVENTORY_FILE = "inventory.yml"
USER = 'cisco'
PWD = 'cisco'
PORT = 443

def main(grpc_host):
    
    hosts = []
    
    with open("mdt_subscriptions.yml", "r") as f:
        mdt_sub = safe_load(f)

    with open(INVENTORY_FILE, "r") as f:
        inventory = safe_load(f)

    for router in inventory['routers']:
        if inventory['routers'][router]['mdt_bgp']:
            hosts.append(inventory['routers'][router]['ip'])

    for subscription in mdt_sub['subscriptions']:
        mdt_sub['subscriptions'][subscription]['rx']['ip'] = grpc_host
    j2_env = Environment(loader=FileSystemLoader("."), trim_blocks=True, autoescape=True)
    template = j2_env.get_template("templates/mdt_xml.jinja2")
    new_config = template.render(data=mdt_sub)

    for host in hosts:

        connect_params = {
            "host": host,
            "username": USER,
            "password": PWD,
            "hostkey_verify": False,
            "allow_agent": False,
            "look_for_keys": False,
            "device_params": {"name": "csr"},
        }

        with manager.connect(**connect_params) as conn:
            print(f"NETCONF session connected: {host}")

            # Perform the update, and if success, print a message
            config_resp = conn.edit_config(target="running", config=new_config)
            if config_resp.ok:
                print(f"Added ({len(mdt_sub['subscriptions'])}) subscriptions")

        print(f"NETCONF session disconnected: {host}")
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: python netconf_mdt_subscription.py <gRPC host ip address>")
        sys.exit(1)

    main(sys.argv[1])