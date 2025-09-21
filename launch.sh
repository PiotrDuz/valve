#!/bin/bash
/home/dzawor/new_venv/bin/python /home/dzawor/valve/main.py | rotatelogs logs.log 100M
