#!/bin/bash
PORT=${PORT:=5000}
INTERVAL=${INTERVAL:=3600}

echo "scrap version 0.2"
#Xvfb :99 -screen 0 1024x768x24 -nolisten tcp &

export FLASK_APP=index.py
echo "starting web service on port $PORT"
#nohup flask run -h 0.0.0.0 -p $PORT --with-threads --no-reload &

echo "getting latest grades"
/opt/echo/app/scrap.py
