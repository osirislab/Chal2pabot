FROM ubuntu:18.04
MAINTAINER John Cunniff

ENV NAME Chal2pabot
ENV REPO_PATH "~/osiris/RED"

RUN echo "Setting challenge path to ${REPO_PATH}"

WORKDIR /${NAME}
COPY . /${NAME}

RUN apt-get update && apt-get install -y apt-utils
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip3 install -r ./requirements.txt
RUN ./chal2pabot.py --init --path ${REPO_PATH}

CMD /${NAME}/chal2pabot.py
