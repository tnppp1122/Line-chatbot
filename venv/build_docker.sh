#!/bin/sh


# read the environment variables from .env.dev
[ -e "$PWD"/.env.dev ] && . "$PWD"/.env.dev


app="docker.test"
docker build -t ${app} .
docker run -p 5000:5000 -d \
  --name=${app} \
  -e FLASK_DEBUG=${FLASK_DEBUG} \
  -v "$PWD":/line_flask_app ${app}
