FROM python:3.7-alpine
MAINTAINER belgacea "https://github.com/belgacea"
RUN apt-get update -y
# TODO install either chrome or firefox (gecko) drivers
RUN apt-get install -y python-pip python-dev build-essential xvfb
RUN mkdir /script
WORKDIR /script
COPY requirements.txt /script/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /script
# TODO cronjob : https://stackoverflow.com/questions/26822067/running-cron-python-jobs-within-docker
# TODO export .env file : https://stackoverflow.com/questions/19331497/set-environment-variables-from-file
CMD ./script/run-env.sh