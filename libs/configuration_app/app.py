from flask import Flask, render_template, request, redirect
import subprocess
import os
import time
from threading import Thread

app = Flask(__name__)
app.debug = True

os.system('service dnsmasq restart') #because it refuses to start upon boot

def scan_wifi_networks():
    iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE)
    ap_list, err = iwlist_raw.communicate()
    ap_array = []

    for line in ap_list.decode('utf-8').rsplit('\n'):
        if 'ESSID' in line:
            ap_ssid = line[27:-1]
            if ap_ssid != '':
                ap_array.append(ap_ssid)
                
    return ap_array

os.system('iwconfig wlan0 mode Managed')
wifi_ap_array=scan_wifi_networks()
os.system('/etc/init.d/hostapd restart')

@app.route('/login')
def login():
    #os.system('iwconfig wlan0 mode Managed')
    #wifi_ap_array = scan_wifi_networks()
    #os.system('/etc/init.d/hostapd restart')
    return render_template('app.html', wifi_ap_array = wifi_ap_array)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return redirect ("http://login.com/login")

@app.route('/manual_ssid_entry')
def manual_ssid_entry():
    return render_template('manual_ssid_entry.html')


@app.route('/save_credentials', methods = ['GET', 'POST'])
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

    return render_template('save_credentials.html', ssid = ssid)




######## FUNCTIONS ##########

#def scan_wifi_networks():
    #iwlist_raw = subprocess.Popen(['iwlist', 'scan'], stdout=subprocess.PIPE)
    #ap_list, err = iwlist_raw.communicate()
    #ap_array = []

    #for line in ap_list.decode('utf-8').rsplit('\n'):
        #if 'ESSID' in line:
            #ap_ssid = line[27:-1]
            #if ap_ssid != '':
                #ap_array.append(ap_ssid)

    #return ap_array

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
    temp_conf_file.write('wpa-ssid' + ssid + '\n')
    temp_conf_file.write('wpa-psk' + wifi_key + '\n')
    temp_conf_file.close

    os.system('mv interfaces /etc/network/interfaces')

def set_ap_client_mode():
    os.system('rm /etc/cron.raspiwifi/aphost_bootstrapper')
    os.system('cp /usr/lib/raspiwifi/reset_device/static_files/apclient_bootstrapper /etc/cron.raspiwifi/')
    os.system('chmod +x /etc/cron.raspiwifi/apclient_bootstrapper')
    os.system('mv /etc/dnsmasq.conf.original /etc/dnsmasq.conf')
    #os.system('mv /etc/network/interfaces.original /etc/network/interfaces')
    #os.system('cp /usr/lib/raspiwifi/reset_device/static_files/isc-dhcp-server.apclient /etc/default/isc-dhcp-server')
    os.system('reboot')

def config_file_hash():
    config_file = open('/etc/raspiwifi/raspiwifi.conf')
    config_hash = {}

    for line in config_file:
        line_key = line.split("=")[0]
        line_value = line.split("=")[1].rstrip()
        config_hash[line_key] = line_value

    return config_hash


if __name__ == '__main__':
    config_hash = config_file_hash()

    if config_hash['ssl_enabled'] == "1":
        app.run(host = '0.0.0.0', port = int(config_hash['server_port']), ssl_context='adhoc')
    else:
        app.run(host = '0.0.0.0', port = int(config_hash['server_port']))
