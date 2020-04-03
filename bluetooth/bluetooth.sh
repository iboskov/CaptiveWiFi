#!/bin/bash
obexpushd -B -o /home/logatec/bluetooth
sleep 5
python3 newtestbt.py
python3 receivedfile.py


