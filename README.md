# NANOG 80 Hackathon (Team Blue)

Our idea for the NANOG 80 Hackathon (17-18th Oct 2020) is to create a system to evaluate BGP events based on a defined compliance policy.  We broke the project into several discrete activities/components:

- Defining the desired BGP policies (Yordan)
- Creating a structured document to describe the policy (Lawrence)
- Designing and configuring a network to test the policy (Yordan)
- Developing a solution to extract and store BGP events using network telemetry (Vladimir)
- Developing a solution to assess the compliance of each BGP event, based on the policy (Lawrence)
- Developing a solution to visualize BGP compliance (Pete)

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-4-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## Contributors ✨

Here's the team!

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

# Our Design principles

- Keep it simple
- Build the absolute minimum to end up with a working solution
- Design as an extensible framework, with examples included


# BGP Policies:

Here are some examples of the policy rules we'd like to assess for a given prefix:

- Validate origin ASN 
- Identify BGP route hijacking 
