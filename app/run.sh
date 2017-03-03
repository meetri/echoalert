#!/bin/bash
#export PATH=$PATH:/opt/echo/drivers
#export DISPLAY=:99
Xvfb :99 -screen 0 640x480x8 -nolisten tcp &
exec python /opt/echo/app/scrap.py
