#!/bin/bash
logs=/home/pi/logs.txt
touch $logs
/usr/bin/python3 /home/pi/app/main.py >>$logs 2>&1
