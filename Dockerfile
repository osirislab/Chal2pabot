FROM ubuntu:18.04
MAINTAINER John Cunniff

ENV NAME="Chal2pabot"
ENV TIMEOUT=10
ENV SLACK_URL=""

RUN echo "Setting challenge path to ${PATH}"

WORKDIR /${NAME}
COPY . /${NAME}

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install -r ./requirements.txt

CMD ./chal2pabot.py --init --path ${PATH} --timeout ${TIMEOUT} --slack-url ${SLACK_URL}
