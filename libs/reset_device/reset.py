#import RPi.GPIO as GPIO
import os
import subprocess
import reset_lib
import socket

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
#serial_last_four = subprocess.check_output(['cat', '/proc/cpuinfo'])[-5:-1].decode('utf-8')
config_hash = reset_lib.config_file_hash()
ssid_prefix = config_hash['ssid_prefix'] + " "
hostapd_reset_required = reset_lib.hostapd_reset_check(ssid_prefix)

def ipaddr():
    try:
        ip=[l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
    except:
        ip=""
    return ip

if hostapd_reset_required == True:
    reset_lib.update_hostapd(ssid_prefix)
    os.system('reboot')

wifi_conn=reset_lib.is_wifi_active()
address=ipaddr()
with open("/etc/resolv.conf") as file:
    if 'nameserver 10.0.0.1' in file.read() and address != "":
        pass
    else:
        if wifi_conn == False:
            reset_lib.reset_to_host_mode()

# This is the main logic loop waiting for a button to be pressed on GPIO 18 for 10 seconds.
# If that happens the device will reset to its AP Host mode allowing for reconfiguration on a new network.
#while True:
    #while GPIO.input(18) == 1:
        #time.sleep(1)
        #counter = counter + 1

        #print(counter)

        #if counter == 9:
            #reset_lib.reset_to_host_mode()

        #if GPIO.input(18) == 0:
            #counter = 0
            #break

    #time.sleep(1)
