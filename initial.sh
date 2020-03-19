#!/bin/bash
FILE="/home/logatec/CaptiveWiFi/initialboot"
apt-get install python3 python3-pip dnsmasq hostapd -y
pip3 install flask
if [ -e "$FILE" ];
then
   ./initial_setup.py
else
   exit 0
fi
