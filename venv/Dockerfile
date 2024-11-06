# pull official base image
FROM python:3.10-alpine3.17

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /line_flask_app

# update the system and add git
RUN apk update && apk add git

# install dependencies
COPY ./requirements.txt /line_flask_app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# copy project
COPY . /line_flask_app

# wait for DB connection, create database, and run Flask app
ENTRYPOINT ["/bin/sh", "-c", "\
    echo 'Waiting for the DBMS to accept connection' && \
    while ! nc -z db $DATABASE_PORT; do \
        sleep 1; \
    done && \
    echo 'Connected to DB, creating database tables...' && \
    python3 manage.py create_db && \
    echo 'Starting Flask...' && \
    flask run --host=0.0.0.0 --port=5000"]

CMD ["tail", "-f", "/dev/null"]
