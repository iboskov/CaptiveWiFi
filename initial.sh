#!/bin/bash
FILE="/home/logatec/CaptiveWiFi/initialboot"

if [ -e "$FILE" ];
then
   ./initial_setup.py
else
   exit 0
fi
