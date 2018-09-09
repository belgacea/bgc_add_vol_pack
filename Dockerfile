FROM python:3.7-alpine

MAINTAINER belgacea "https://github.com/belgacea"

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.7/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.7/community" >> /etc/apk/repositories
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y \
    wget \
    python-pip \
    python-dev\
    build-essential \
    cron \
    # chromium web driver
    chromium \
    chromium-chromedriver \
    # headless browser support
    xvfb \
    # needed to launch firefox
    libgl1-mesa-glx \
    libgtk-3-dev
# Firefox web drive
ARG FIREFOX_VERSION=61.0.2
RUN wget --no-verbose -O /tmp/firefox.tar.bz2 https://download-installer.cdn.mozilla.net/pub/firefox/releases/$FIREFOX_VERSION/linux-x86_64/en-US/firefox-$FIREFOX_VERSION.tar.bz2 \
   && rm -rf /opt/firefox \
   && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
   && rm /tmp/firefox.tar.bz2 \
   && mv /opt/firefox /opt/firefox-$FIREFOX_VERSION \
   && ln -fs /opt/firefox-$FIREFOX_VERSION/firefox /usr/bin/firefox
ARG GK_VERSION=v0.21.0
RUN wget --no-verbose -O /tmp/geckodriver.tar.gz http://github.com/mozilla/geckodriver/releases/download/$GK_VERSION/geckodriver-$GK_VERSION-linux64.tar.gz \
   && rm -rf /opt/geckodriver \
   && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
   && rm /tmp/geckodriver.tar.gz \
   && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
   && chmod 755 /opt/geckodriver-$GK_VERSION \
   && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver

RUN mkdir /script
WORKDIR /script
COPY . /script
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# TODO check cronjob : https://stackoverflow.com/questions/26822067/running-cron-python-jobs-within-docker
# TODO export .env file : https://stackoverflow.com/questions/19331497/set-environment-variables-from-file
# add crontab file in the cron directory
ADD cronjobs /etc/cron.d/cronjobs
# give execution rights to the cronjob file
RUN chmod 0644 /etc/cron.d/cronjobs
# set cronjobs
RUN /usr/bin/crontab /etc/cron.d/cronjobs
# run cron at container startup
CMD cron && tail -f /dev/null