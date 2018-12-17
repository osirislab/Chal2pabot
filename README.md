# Chal2pabot
<p align="center">
   <img src="https://raw.githubusercontent.com/osirislab/Chal2pabot/master/logo.png" width=500 title="hover text">
<p>


# Description
- Chal2pabot is a simple bot for maintaining infrastructure durring a ctf. All it does is make sure certain ip's are responding to connections. 

# Configuration
```
docker build -t Chal2pabot .
docker run --name Chal2pabot -e PATH="/path/to/repo/or/json" Chal2pabot
```
- optional enviorment variables are TIMOUT and SLACK_URL

### Maintainer
- John Cunniff
- jmc1283@nyu.edu
