FROM python:3.7-alpine
MAINTAINER John Cunniff

WORKDIR /bot
COPY . .

RUN pip3 install -r ./requirements.txt

CMD echo $SLACK; ./chal2pabot.py --timeout 10 --slack-url ${SLACK}
