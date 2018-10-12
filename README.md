# Chal2pabot
- Chal2pabot is a simple bot for maintaining infrastructure durring a ctf. All it does is make sure certain ip's are responding to connections. 

# Configuration
- The enviorment variable REPO_PATH must be set in Dockerfile to point to the directory that contains all the challenges.
- Any challenge's that you would like the chalbot to check, must have a challenge.json in the repo with both a 'name' and 'url' element. You can also just go in and edit the generated state.json in the docker container to overwrite the names and/or urls of challenges.

### Maintainer
- John Cunniff
- jmc1283@nyu.edu
