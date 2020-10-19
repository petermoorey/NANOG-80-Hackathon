# NANOG 80 Hackathon

Our idea for the NANOG 80 Hackathon (17-18th Oct 2020) is to create a system to evaluate BGP events based on a defined policy.

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/TheBirdsNest"><img src="https://avatars3.githubusercontent.com/u/31070227?v=4" width="100px;" alt=""/><br /><sub><b>Lawrence Bird</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=TheBirdsNest" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/yordangit12"><img src="https://avatars1.githubusercontent.com/u/47042822?v=4" width="100px;" alt=""/><br /><sub><b>yordangit12</b></sub></a><br /><a href="#infra-yordangit12" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
    <td align="center"><a href="https://github.com/VladimirGHC"><img src="https://avatars1.githubusercontent.com/u/72935381?v=4" width="100px;" alt=""/><br /><sub><b>Vladimir Yakovlev</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=VladimirGHC" title="Code">💻</a></td>
    <td align="center"><a href="https://www.linkedin.com/in/pmoorey"><img src="https://avatars3.githubusercontent.com/u/10014623?v=4" width="100px;" alt=""/><br /><sub><b>Peter Moorey</b></sub></a><br /><a href="https://github.com/petermoorey/NANOG-80-Hackathon/commits?author=petermoorey" title="Code">💻</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->



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
