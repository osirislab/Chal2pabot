FROM python:3.7-alpine
MAINTAINER John Cunniff

WORKDIR /bot
COPY . .

RUN pip3 install -r ./requirements.txt

CMD ./chal2pabot.py --timeout 30 --slack-url ${SLACK}
