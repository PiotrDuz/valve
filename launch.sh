#!/bin/bash
#not needed, app is launched directly from systemd service
/home/dzawor/new_venv/bin/python /home/dzawor/valve/main.py 2>&1 | rotatelogs -t /home/dzawor/logs.log 100M
