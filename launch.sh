#!/bin/bash
while true; do find /home/dzawor/logs.txt -size +100M -delete; sleep 60; done &
stdbuf -oL /home/dzawor/new_venv/bin/python /home/dzawor/valve/main.py &>> /home/dzawor/logs.txt

