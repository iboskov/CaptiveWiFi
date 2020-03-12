import os
import fileinput

def copy_configs():
	os.system('mkdir /usr/lib/raspiwifi')
	os.system('mkdir /etc/raspiwifi')
	os.system('cp -a /home/logatec/CaptiveWiFi/libs/* /usr/lib/raspiwifi/')
	os.system('cp /usr/lib/raspiwifi/reset_device/reset_lib.py /usr/lib/raspiwifi/configuration_app/')
	os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm -f ./tmp/*')
	os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf /etc/hostapd/')
	os.system('mv /etc/network/interfaces /etc/network/interfaces.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/interfaces /etc/network/')
	os.system('mv /etc/resolv.conf /etc/resolv.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/resolv.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.service /etc/systemd/system/')
	os.system('systemctl daemon-reload')
	os.system('systemctl enable raspiwifi')
	os.system('touch /usr/lib/raspiwifi/APMODE')
	os.system('chmod +x /usr/lib/raspiwifi/reset_device/static_files/aphost_bootstrapper')
	os.system('mv /usr/lib/raspiwifi/reset_device/static_files/raspiwifi.conf /etc/raspiwifi')
	
	with fileinput.input("/etc/default/hostapd", inplace=True) as file:
		for line in file:
			print(line.replace('#DAEMON_CONF=""', 'DAEMON_CONF="/etc/hostapd/hostapd.conf"'), end='') #change the file hostapd in /etc/default/ so that it knows the exact location of hostapd.conf
		file.close()
	
		
def checkid(): #function to get the machine id
	with open ('/etc/machine-id') as file: #open the file machine-id
		line = file.readline().strip() #read only the first line of the file and strip the newline
		return line[-8:] #return the last eight letters from the line

		
id = checkid() #save the output of checkid() as a string variable 
	
def update_main_config_file(entered_ssid, server_port_choice):
	if entered_ssid != "": #check if entered_ssid is empty, if so default APname is LGTC-AP
		os.system('sed -i \'s/LGTC-AP/' + entered_ssid + '/\' /etc/raspiwifi/raspiwifi.conf')
	else:
		with fileinput.input("/etc/raspiwifi/raspiwifi.conf", inplace=True) as file: #open the raspiwifi.conf file
			for line in file: #read the file line by line
				print(line.replace('ssid_prefix=LGTC-AP', 'ssid_prefix=LGTC_' + id), end='') #when the string ssid_prefix=LGTC-AP is found overwrite it with LGTC_ and the id of the machine, this is the new APname
	if server_port_choice != "": #check if server_port_choice is empty, if so default port is 80
		with fileinput.input("/etc/raspiwifi/raspiwifi.conf", inplace=True) as file: #open the raspiwifi.conf file
			for line in file: #read the file line by line
				print(line.replace('server_port=80', 'server_port=' + server_port_choice), end='') #when the string server_port=80 is found overwrite it with user's inputed port
