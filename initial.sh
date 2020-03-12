#!/bin/bash
PATH="/home/logatec/CaptiveWiFi/"
FILE="/home/logatec/CaptiveWiFi/initialboot"

if [ -e "$FILE" ];
then
   cd $PATH
   ./initial_setup.py
else
   exit 0
fi
