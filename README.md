# NANOG 80 Hackathon

Our idea for the NANOG 80 Hackathon (17-18th Oct 2020) was to create *a system for evaluating BGP events based on rules defined in a compliance policy*.  

Our personal goals during the hackathon were to:

- Evaluate various technology stacks
- Explore network telemetry capabilities
- Create a network to showcase routing scenarios
- Provide real-time evaluation of BGP routes to detect:
  * Poorly configured route-maps
  * Incorrect provider policies
  * Route hijacking

## Project organization

To deliver the solution as a team, we broke the project into several discrete activities/components.  We used GitHub to track the work items and assign responsibilities:

- Defining the desired BGP policies (Yordan)
- Structured document to describe the policy (Yordan/Lawrence)
- Designing and configuring the network topology (Yordan)
- Extract and store BGP events using network telemetry (Vladimir)
- Assess the compliance of each BGP event (Lawrence)
- Visualize BGP compliance (Pete)

We were able to successfully create a working solution, and delivered a 15 minute presentation to the other NANOG Hackathon participants.  You can find a copy of the presentation [here](https://github.com/petermoorey/NANOG-80-Hackathon/blob/main/docs/NANOG%20Presentation.pdf).

## Contributors

Here's the team!

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/TheBirdsNest"><img src="https://avatars3.githubusercontent.com/u/31070227?v=4" width="100px;" alt=""/><br /><sub><b>Lawrence Bird</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=TheBirdsNest" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/yordangit12"><img src="https://avatars1.githubusercontent.com/u/47042822?v=4" width="100px;" alt=""/><br /><sub><b>yordangit12</b></sub></a><br /><a href="#infra-yordangit12" title="Infrastructure (Hosting, Build-Tools, etc)">💻</a></td>
    <td align="center"><a href="https://github.com/VladimirGHC"><img src="https://avatars1.githubusercontent.com/u/72935381?v=4" width="100px;" alt=""/><br /><sub><b>Vladimir Yakovlev</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=VladimirGHC" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/pmoorey"><img src="https://avatars3.githubusercontent.com/u/10014623?v=4" width="100px;" alt=""/><br /><sub><b>Peter Moorey</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=petermoorey" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

## Our design principles

- Keep it simple
- Build the absolute minimum to end up with a working solution
- Design as an extensible framework, with examples included

## High-level design

Before starting we sat down together and agreed how the solution should be build.

![High-level Design](https://github.com/petermoorey/NANOG-80-Hackathon/blob/main/docs/SystemDesign.drawio.svg)

## Defining the desired BGP policies

Here are some examples of the policy rules we'd like to assess for a given prefix:

- Validate correct origin ASN 
- Identify instances of BGP route hijacking
- Verify correct provider route handling based on BGP community values

## Policy definition

We decided to use a YAML document to describe the desired policy:

```yaml
# BGP RIB Compliance Policy file for demo lab

root_source: Cisco-IOS-XE-bgp-oper:bgp-state-data/bgp-route-vrfs/bgp-route-vrf
root_path: bgp_route_af/bgp_route_filter/bgp_route_entry/bgp_path_entry/
regions:
    emea:
        - 10.200.49.9       # Bern
        - 10.200.49.10      # Rome
    americas:
        - 10.200.49.5       # Boston
        - 10.200.49.6       # Quito
    external:
        - 10.200.49.4       # Americas DC
        - 10.200.49.8       # Europe DC
policy:
    0.0.0.0/0:                          # Match default route
        match: explicit                 # Match type is explicit. RIB prefix must match 0.0.0.0/0 exactly
        region: americas                # Region to monitor for RIB updates on
        attributes:                     # List of attributes to evaluate and expected values
            community: 100:1            # Community value expected in RIB update
    0.0.0.0/0:                          # Match default route
        match: explicit                 # Match type is explicit. RIB prefix must match 0.0.0.0/0 exactly
        region: emea                    # Region to monitor for RIB updates on
        attributes:                     # List of attributes to evaluate and expected values
            community: 100:2            # Community value expected in RIB update
    192.168.0.0/16:
        match: any                      # any match will include any network prefix that is within the subnet, or the subnet itself
        region: external
        attributes:
            origin: 100
            as_path: 13979 13979
    150.0.0.0/16:
        match: any
        region: external
        attributes:
            origin: 150
```

## Designing and configuring the network topology

Here's our network design; the requirement was to be able to simulate all our BGP policy compliance scenarios.

![Network Topology](https://github.com/petermoorey/NANOG-80-Hackathon/blob/main/docs/images/Network%20Topology.png)

## Extract and store BGP events using network telemetry

In order to assess compliance we needed to extract BGP events from our network devices.  We used Netconf and Model Driven Telemetry (MDT) to obtain BGP data and insert it into a time series database (InfluxDB) via Telegraf.

```yaml
---
subscriptions:
  100:
    xpath: "/bgp-ios-xe-oper:bgp-state-data/bgp-route-vrfs"
    period: 3000
    sourcevrf: "mgmt"
    rx:
      ip: "10.0.0.1" # Dummy IP address for now, Netconf MDT Subsription script changes it to the IP address which is supplied to the script
      tcp_port: 35005
```

## Assess the compliance of each BGP event

Each BGP event in InfluxDB is assessed according to the desired policy, rules are evaluated top-down, like an ACL.  The compliance results are stored in a separate table in InfluxDB for visualization.

```python
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
```

## Visualize BGP compliance

To visualize the state of policy compliance, we experimented with Chronograf and Plotly/Dash.  The visualizations count the sum of non-compliant prefixes and group by router or prefix.

Screenshot of Chronograf dashboard:
![Screenshot of Chronograf](https://github.com/petermoorey/NANOG-80-Hackathon/blob/main/docs/images/Chronograf.jpg?raw=true)

Screenshot of Python Plotly/Dash dashboard:
![Screenshot of Chronograf](https://github.com/petermoorey/NANOG-80-Hackathon/blob/main/docs/images/Plotly.jpg?raw=true)