# NANOG 80 Hackathon
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-2-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/TheBirdsNest"><img src="https://avatars3.githubusercontent.com/u/31070227?v=4" width="100px;" alt=""/><br /><sub><b>Lawrence Bird</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=TheBirdsNest" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/yordangit12"><img src="https://avatars1.githubusercontent.com/u/47042822?v=4" width="100px;" alt=""/><br /><sub><b>yordangit12</b></sub></a><br /><a href="#infra-yordangit12" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=yordangit12" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!