# NANOG 80 Hackathon

Create a system to evaluate BGP events based on a defined policy.

# Design principles

- Keep it simple
- Build the absolute minimum to end up with a working solution
- Design as an extensible framework, with examples included


# Example Policy Compliance Object:

```
json_data = [
    {
        "measurement": "routingCompliance",
        "tags": {
            "prefix": "192.168.0.0/24",
            "source": "10.200.49.8",
            "as_path": ""
        },
        "time": datetime.now(),
        "fields": {
                "as_origin_compliance": 1,
                "community_compliance": 0,
                "weight_compliance": 0,
                "med_compliance": 0,
        }
    }
]
```
