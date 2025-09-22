#!/bin/bash
/home/dzawor/new_venv/bin/python /home/dzawor/valve/main.py 2>&1 | rotatelogs /home/dzawor/logs.log 100M
