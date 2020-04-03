#!/usr/bin/python3

import os
import sys
import setup_lib
import time

startT=time.time()
if os.getuid():
    sys.exit('You need root access to install!')


#os.system("clear")
entered_ssid = ""
print()
server_port_choice = ""
print()
install_ans = "y"

if(install_ans.lower() == 'y'):
	#setup_lib.install_prereqs()
	setup_lib.copy_configs()
	setup_lib.update_main_config_file(entered_ssid, server_port_choice)
	#os.system("systemctl start raspiwifi.service")
else:
	print()
	sys.exit()

#os.system("clear")
print()
os.system("rm -rf /home/logatec/CaptiveWiFi/initialboot")
endT=time.time()
print(endT-startT, file=open("initial.txt", "a"))
#os.system("reboot")
