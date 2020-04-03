import os
import fileinput
import time
import sys
import re


def createfile(ssid,wpapsk):
        temp_conf_file=open('test', 'w')
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
        temp_conf_file.write('wpa-psk ' + wpapsk + '\n')
        temp_conf_file.close()

        os.system('mv test /home/logatec/testbt')

startt=time.time()
counter = 0;
for file in os.listdir("/home/logatec/bluetooth"):
        while counter <= 5:
                if file.endswith('.html') is True:
                        file = open ('/home/logatec/bluetooth/bluetooth_content_share.html', 'r')
                        for line in file: 
                                text=line.split('<body>') [1]
                                ssid=text.split('<br>') [0]
                                ssid=re.sub(r'<.+?>','', ssid)
                                wpapsk=text.split('<br>') [1]
                                wpapsk=re.sub(r'<.+?>','', wpapsk)
                                createfile(ssid,wpapsk)
                        break
                        #sys.exit()
                elif file.endswith('.txt') is True:
                        file = open('/home/logatec/bluetooth/*.txt', 'r')
                        i=0;
                        for line in file:
                                if i == 0:
                                        ssid = line
                                        i+=1
                                else:
                                        wpapsk = line
                                createfile(ssid,wpapsk)
                                sys.exit()
                else:   
                        time.sleep(5)
endt=time.time()
print(endt-startt, file=open("receivedbttime.txt", "a"))
sys.exit()

