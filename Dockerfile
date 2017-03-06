FROM centos:7
LABEL maintainer "Demetrius Bell <meetri@gmail.com>"

RUN yum install -y gcc epel-release \
&& yum install -y python-pip python-devel Xvfb bzip2 fontconfig\
&& pip install --upgrade pip \
&& pip install flask selenium psycopg2 twilio

ENV DISPLAY :99
RUN dbus-uuidgen > /etc/machine-id

RUN mkdir -p /opt/echo/drivers /opt/echo/logs /usr/local/phantomjs

ENV PHANTOMJS_VER=2.1.1
RUN cd /opt && curl -LO https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-${PHANTOMJS_VER}-linux-x86_64.tar.bz2 \
&& tar -xvjf /opt/phantomjs-${PHANTOMJS_VER}-linux-x86_64.tar.bz2 -C /usr/local/phantomjs --strip-components=1 \
&& ln -s /usr/local/phantomjs/bin/phantomjs /usr/bin/phantomjs

COPY app /opt/echo/app
RUN chmod +x /opt/echo/app/scrap.py /opt/echo/app/run.sh

WORKDIR /opt/echo/app

ENTRYPOINT ["/opt/echo/app/run.sh"]
