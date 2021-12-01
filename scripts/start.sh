#!/bin/bash

if [ "$ENVFLAG" == "prod" ];then
   python main.py --config-file=etc/prod/config
elif [ "$ENVFLAG" == "beta" ];then
   python main.py --config-file=etc/beta/config
else
   python main.py --config-file=etc/dev/config
fi
