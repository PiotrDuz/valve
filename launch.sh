#!/bin/bash
/home/pi/new_venv/bin/python /home/pi/valve/main.py | rotatelogs logs.log 100M
