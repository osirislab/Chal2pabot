# Python
MAIN_NAME=app.py
ENV_NAME=venv
PYTHON_VERSION=`which python3`

# Docker
DOCKER_IMAGE_NAME=chalbot_api
DOCKER_OPTIONS=--rm -it
DOCKER=docker
DOCKER_COMPOSE=docker-compose

.PHONY: run setup build rund killd clean cleand

all: build

build:
	${DOCKER} build -t ${DOCKER_IMAGE_NAME} .

rund: killd
	${DOCKER} run ${DOCKER_OPTIONS} --name ${DOCKER_IMAGE_NAME} ${DOCKER_IMAGE_NAME}

killd:
	if [ -z "$(${DOCKER} ps -q) | grep ${DOCKER_IMAGE_NAME}" ]; then \
		${DOCKER} kill ${DOCKER_IMAGE_NAME}; \
	fi

setup:
	if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
	if [ -a requirements.txt ]; then \
		touch requirements.txt; \
	fi
	which virtualenv && pip install virtualenv || true
	virtualenv -p ${PYTHON_VERSION} ${ENV_NAME}
	./${ENV_NAME}/bin/pip install -r requirements.txt

run:
	if [ ! -d ${ENV_NAME} ]; then \
		make setup; \
	fi
	./${ENV_NAME}/bin/python ${MAIN_NAME}

cleand: killd
	echo 'y' | ${DOCKER} system prune
	if [ -n "`${DOCKER} image list -q | grep ${DOCKER_IMAGE_NAME}`" ]; then \
		${DOCKER} rmi ${DOCKER_IMAGE_NAME}; \
	fi

clean:
	if [ -d ${ENV_NAME} ]; then \
		rm -rf ${ENV_NAME}; \
	fi
	if [ -n "`find . -name __pycache__`" ]; then \
		rm -rf `find . -name __pycache__`; \
	fi


test:
	curl -H "Content-Type: application/json" 'http://localhost:5000/chal/new' \
	  --data '{"url": "http://web.chal.csaw.io:1000/", "name": "name1"}'

	curl 'http://localhost:5000/chal/list'

	curl -H "Content-Type: application/json" 'http://localhost:5000/chal/report' \
	  --data '{"OFFLINE_CHALLENGES":["name1"], "CHALLENGE_MAP":{"name1":"http://web.chal.csaw.io:1000/"}}'

	curl 'http://localhost:5000/chal/list'

	curl -H "Content-Type: application/json" 'http://localhost:5000/chal/del' \
	  --data '{"name": "name1"}'
