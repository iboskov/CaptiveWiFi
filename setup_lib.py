import os
import fileinput

def install_prereqs():
	os.system('clear')
	os.system('apt update')
	os.system('clear')
	os.system('apt install python3 python3-pip dnsmasq hostapd -y')
	os.system('clear')
	print("Installing Flask web server...")
	print()
	os.system('pip3 install flask')
	os.system('clear')

def copy_configs():
	os.system('mkdir /usr/lib/raspiwifi')
	os.system('mkdir /etc/raspiwifi')
	os.system('cp -a libs/* /usr/lib/raspiwifi/')
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
			print(line.replace('#DAEMON_CONF=""', 'DAEMON_CONF="/etc/hostapd/hostapd.conf"'), end='')
		file.close()
	
		
def checkid():
	with open ('/etc/machine-id') as file:
		for line in file:
			return line

		
id = checkid()
	
def update_main_config_file(entered_ssid, auto_config_choice, auto_config_delay, ssl_enabled_choice, server_port_choice):
	if entered_ssid != "":
		os.system('sed -i \'s/LGTC-AP/' + entered_ssid + '/\' /etc/raspiwifi/raspiwifi.conf')
	else:
		with fileinput.input("/etc/raspiwifi/raspiwifi.conf", inplace=True) as file:
			for line in file:
				print(line.replace("ssid_prefix=LGTC-AP", "ssid_prefix=LGTC_" + id), end='')
			file.close()
		
	if auto_config_choice.lower() == "y":
		os.system('sed -i \'s/auto_config=0/auto_config=1/\' /etc/raspiwifi/raspiwifi.conf')
	if auto_config_delay != "":
		os.system('sed -i \'s/auto_config_delay=300/auto_config_delay=' + auto_config_delay + '/\' /etc/raspiwifi/raspiwifi.conf')
	if ssl_enabled_choice.lower() == "y":
		os.system('sed -i \'s/ssl_enabled=0/ssl_enabled=1/\' /etc/raspiwifi/raspiwifi.conf')
	if server_port_choice != "":
		os.system('sed -i \'s/server_port=80/server_port=' + server_port_choice + '/\' /etc/raspiwifi/raspiwifi.conf')
