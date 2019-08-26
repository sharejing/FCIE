#!/usr/bin/env bash

nohup python /root/FCIE/routes_java.py >> /root/log_FCIE/nohup_java.out &
nohup python /root/FCIE/routes_python.py >> /root/log_FCIE/nohup_python.out &
