import os
import fileinput
import urllib.request, urllib.error
import time

def config_file_hash():
	config_file = open('/etc/raspiwifi/raspiwifi.conf')
	config_hash = {}

	for line in config_file:
		line_key = line.split("=")[0]
		line_value = line.split("=")[1].rstrip()
		config_hash[line_key] = line_value

	return config_hash

def hostapd_reset_check(ssid_prefix):
	hostapd_conf = open('/etc/hostapd/hostapd.conf', 'r')
	reset_required = True

	for line in hostapd_conf:
	    if ssid_prefix in line:
	        reset_required = False

	return reset_required

def update_hostapd(ssid_prefix):
	os.system('cp -a /usr/lib/raspiwifi/reset_device/static_files/hostapd.conf /etc/hostapd/')

	with fileinput.input("/etc/hostapd/hostapd.conf", inplace=True) as file:
		for line in file:
			print(line.replace("beaglebone", ssid_prefix), end='') #check if the APname is the same as the entered_ssid, if not replace it
		file.close()

def is_wifi_active(): #function that checks if there is active internet connection
	counter = 0
	while counter <10: #try 10 times to see if there is internet conection
		try:
			urllib.request.urlopen("http://google.com") #ping google and wait for the response
		except urllib.error.URLError as err: #if there isn't a positive response, then there is no connection
			wifi_active = False
		else:
			wifi_active = True #if there is a positive response, then there is internet connection and the loop should break
			break
		time.sleep(10) #try again after 10 seconds
		counter = counter+1
	return wifi_active

def reset_to_host_mode():
	os.system('rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
	os.system('rm /etc/cron.raspiwifi/apclient_bootstrapper')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/interfaces /etc/network/')
	os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.conf.original')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/dnsmasq.conf /etc/')
	os.system('cp /usr/lib/raspiwifi/reset_device/static_files/resolv.conf /etc/')
	os.system('touch /usr/lib/raspiwifi/APMODE')
	os.system('reboot')
