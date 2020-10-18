from yaml import safe_load
from netmiko import Netmiko

INVENTORY_FILE = "inventory.yml"
USER = 'cisco'
PWD = 'cisco'

def set_config(ip, config):

    device = {
        "device_type": "cisco_xe",
        "ip": ip,
        "username": USER,
        "password": PWD,
        "port": 22,
    }

    net_connect = Netmiko(**device)
    output = net_connect.send_config_set(config)
    print(output)
    net_connect.disconnect()

def main():

    with open(INVENTORY_FILE, "r") as f:
        inventory = safe_load(f)

    for router in inventory['routers']:
        if inventory['routers'][router]['mdt_enable']:
            ip = inventory['routers'][router]['ip']
            config = ["ip http secure-server", "restconf", "netconf ssh", "netconf-yang"]
            set_config(ip, config)

if __name__ == "__main__":
    main()