import subprocess
import os
#line=f.readline()-e
#os.system("echo 'power on\n' 'discoverable on\n' 'pairable on\n' 'quit/n' | bluetoothctl | grep 'Device' | cut -d ' ' -f 4 > devices")
#with open ("devices", "r") as f
os.system(" { echo -e 'power on\n'; echo -e 'discoverable on\n'; echo -e 'pairable on\n'; sleep 20; echo -e 'devices\n';} | bluetoothctl | grep 'Device ' | cut -d ' ' -f 4 > devices")
with open("devices") as d:
        for line in d:
                line=d.readline()
                #child.sendline('trust ' + line)


#proc = subprocess.getoutput("echo 'power on\n' 'pairable on\n' 'devices\n' | bluetoothctl | grep 'Device ' | cut -d ' ' -f 2 ")
#print (proc)


