FROM centos:7
LABEL maintainer "Demetrius Bell <meetri@gmail.com>"

RUN yum install -y gcc epel-release \
&& yum install -y python-pip python-devel Xvfb firefox\
&& pip install --upgrade pip \
&& pip install flask selenium psycopg2

ENV DISPLAY :99
RUN dbus-uuidgen > /etc/machine-id

RUN mkdir -p /opt/echo/drivers /opt/echo/logs
COPY app /opt/echo/app
RUN chmod +x /opt/echo/app/scrap.py /opt/echo/app/run.sh

ADD https://github.com/mozilla/geckodriver/releases/download/v0.14.0/geckodriver-v0.14.0-linux64.tar.gz /opt/echo/drivers
RUN cd /opt/echo/drivers && tar -xvzf gecko*.tar.gz

WORKDIR /opt/echo/app

ENTRYPOINT ["/opt/echo/app/run.sh"]
