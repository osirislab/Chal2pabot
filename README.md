# Chal2pabot
![alt text](https://raw.githubusercontent.com/osirislab/Chal2pabot/master/chal2pa.png)


# Description
- Chal2pabot is a simple bot for maintaining infrastructure durring a ctf. All it does is make sure certain ip's are responding to connections. 

# Configuration
- The enviorment variable REPO_PATH must be set in Dockerfile to point to the directory that contains all the challenges.
- Any challenge's that you would like the chalbot to check, must have a challenge.json in the repo with both a 'name' and 'url' element.
  - If making challenge.json's if an inconvenience to you, just go in and edit the generated CHALLENGE_MAP element in the state.json in the docker container to the names and urls of the challenges that you want. Just make sure to restart the container!

### Maintainer
- John Cunniff
- jmc1283@nyu.edu
