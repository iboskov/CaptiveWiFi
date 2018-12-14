#!/bin/bash

FILE="/home/logatec/RaspiWiFi/initialboot"

if [ -e "$FILE" ];
then
   python3 /home/logatec/RaspiWiFi/initial_setup.py
else
   exit 0
fi
