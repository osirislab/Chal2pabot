FROM python:3.7-alpine

WORKDIR /opt/app

COPY requirements.txt .
RUN apk --update --no-cache add mariadb-client && pip3 install -r requirements.txt

COPY . .

CMD ./entrypoint.sh
