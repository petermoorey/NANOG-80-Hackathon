# NANOG 80 Hackathon

Create a system to evaluate BGP events based on a defined policy

# Design principles

- Keep it simple
- Build the absolute minimum to end up with a working solution
- Design as an extensible framework, with examples included


# Example Database Object:

```
{
   "prefix":"10.1.1.0/24",
   "timestamp":"2732973822",
   "attrs":[
      {
         "name":"med",
         "value":30,
         "compliance":"true"
      },
      {
         "name":"as_origin",
         "value":72,
         "compliance":"false"
      }
   ]
}
```