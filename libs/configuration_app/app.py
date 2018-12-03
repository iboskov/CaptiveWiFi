from flask import Flask, render_template, request, redirect
import subprocess
import os
import time
from threading import Thread
import reset_lib
import sys

app = Flask(__name__)
app.debug = True

os.system('service dnsmasq restart')  # because it refuses to start upon boot


def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE) #run the command iwlist scan
    ap_list, err = iwlist_raw.communicate()
    ap_array = [] #create a list where the output of the command will be saved

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line: #find the ESSID in everyline
            if 'x00' in line: #if there is an ESSID which has x00 as a name than skip it (this is a hidden ESSID)
                pass
            else:
                ap_ssid = line[27:-1]
                if ap_ssid != '': #save every ESSID that is not an empty string
                    ap_array.append(ap_ssid)
                
    return ap_array

config_hash = reset_lib.config_file_hash() 
ssid_prefix = config_hash['ssid_prefix'] + " "
hostapd_reset_required = reset_lib.hostapd_reset_check(ssid_prefix)

if hostapd_reset_required == True: #check if the APname of the hostapd and the APname of the raspiwifi.conf are the same
    reset_lib.update_hostapd(ssid_prefix) #if not, overwrite hostapd to have the same name and reboot the device
    os.system('reboot')

os.system('iwconfig wlan0 mode Managed') #put the wlan0 interface in Managed mode so that is able to scan wifi networks
wifi_ap_array = scan_wifi_networks() #save the output of the scan_wifi_networks as a list
os.system('/etc/init.d/hostapd restart') #restart the hostapd service so that the AP will be shown


@app.route('/setup')
def login():
    return render_template('app.html', wifi_ap_array=wifi_ap_array)


@app.route('/', defaults={'path': ''}) #this is where the redirection happens
@app.route('/<path:path>') #redirect evry url with its subpaths to the one below
def index(path):
    return redirect("http://10.0.0.1/setup")


@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')


@app.route('/save_credentials', methods=['GET', 'POST'])
def save_credentials():
    ssid = request.form['ssid']
    wifi_key = request.form['wifi_key']

    create_wpa_supplicant(ssid, wifi_key)

    # Call set_ap_client_mode() in a thread otherwise the reboot will prevent
    # the response from getting to the browser
    def sleep_and_start_ap():
        time.sleep(2)
        set_ap_client_mode()

    t = Thread(target=sleep_and_start_ap)
    t.start()

    return render_template('save_credentials.html', ssid=ssid)


######## FUNCTIONS ##########


def create_wpa_supplicant(ssid, wifi_key):
    temp_conf_file = open('interfaces', 'w')

    temp_conf_file.write('auto lo\n')
    temp_conf_file.write('iface lo inet loopback\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('iface usb0 inet static\n')
    temp_conf_file.write('address 192.168.7.2\n')
    temp_conf_file.write('netmask 255.255.255.252\n')
    temp_conf_file.write('network 192.168.7.0\n')
    temp_conf_file.write('gateway 192.168.7.1\n')
    temp_conf_file.write('\n')
    temp_conf_file.write('auto wlan0\n')
    temp_conf_file.write('iface wlan0 inet dhcp\n')
    temp_conf_file.write('wpa-ssid ' + ssid + '\n')
    temp_conf_file.write('wpa-psk ' + wifi_key + '\n')
    temp_conf_file.close()

    os.system('mv interfaces /etc/network/interfaces')


def set_ap_client_mode():
    os.system('rm /etc/cron.raspiwifi/aphost_bootstrapper')
    os.system('mv /etc/dnsmasq.conf.original /etc/dnsmasq.conf')
    os.system('rm -rf /usr/lib/raspiwifi/APMODE')
    os.system('reboot')


if __name__ == '__main__':
    if os.path.exists('/usr/lib/raspiwifi/APMODE') is True: #check if the file APMODE exists
        config_hash = reset_lib.config_file_hash()
        app.run(host = '0.0.0.0', port = int(config_hash['server_port'])) #if the file exists that means that the device is booted in host mode and waiting to be configured
    else:
        wifi_conn = reset_lib.is_wifi_active() #if the file does not exist that means the device was booted in client mode
        if wifi_conn == True: #check if the device has internet connection, and if it does, exit
            sys.exit()
        else:
            reset_lib.reset_to_host_mode() #if the device does not have internet connection reset it to host mode and reconfigure it
