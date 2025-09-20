#!/bin/bash
/usr/bin/python3 /home/pi/app/main.py | rotatelogs logs.log 100M
