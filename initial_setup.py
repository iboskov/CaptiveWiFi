import os
import sys
import setup_lib


if os.getuid():
    sys.exit('You need root access to install!')


os.system('clear')
print()
print()
print("###################################")
print("##### RaspiWiFi Intial Setup  #####")
print("###################################")
print()
print()
entered_ssid = ""
print()
server_port_choice = ""
print()
print()
install_ans = "y"

if(install_ans.lower() == 'y'):
	setup_lib.install_prereqs()
	setup_lib.copy_configs()
	setup_lib.update_main_config_file(entered_ssid, server_port_choice)
	os.system("touch /home/logatec/initial_boot")
else:
	print()
	print()
	print("===================================================")
	print("---------------------------------------------------")
	print()
	print("RaspiWiFi installation cancelled. Nothing changed...")
	print()
	print("---------------------------------------------------")
	print("===================================================")
	print()
	print()
	sys.exit()

os.system('clear')
print()
print()
print("#####################################")
print("##### RaspiWiFi Setup Complete  #####")
print("#####################################")
print()
print()
print("Initial setup is complete. A reboot is required to start in WiFi configuration mode...")
os.system('reboot')
