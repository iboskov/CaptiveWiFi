import os
import pexpect
import subprocess
import time
import sys

start=time.time()
child=pexpect.spawn("bluetoothctl")
child.send("power on\n")
child.send("agent on\n")
child.send("default-agent\n")
child.send("discoverable on\n")
child.send("pairable on\n")
r=child.readline()
bl=True

while bl==True:
                r=child.readline()
                print(r)
                if b'Request confirmation' in r:
                        print("ok")
                        child.send('yes\n')
                        bl=False
                        while b'Authorize service' in r:
                                child.send('yes\n')
                        while b'Paired: yes' not in r:
                                r=child.readline()
                                if b'Device' in r:
                                        subprocess.getoutput("echo 'devices\n' | bluetoothctl | grep 'Device ' | cut -d ' ' -f 2 > devices") 
                                        #with open("devices", "r") as f:
                                        #        lines = f.readlines()
                                        #with open("devices", "w") as f:
                                        #        for line in lines:
                                        #                if line.strip("\n") != "^[[K[^[[0;92mNEW^[[0m]":
                                        #                        f.write(line)
                                        d = open("devices", "r")
                                        for line in d:
                                                child.send('trust ' + line)
                                                #print (p, file=open("devices","w"))
                                                    #with open("devices") as d:
                                                        #for line in d:
                                                            #child.sendline('trust ' + line)

        #print (r)
                        child.sendline('quit')
end=time.time()
print(end-start, file=open("bts.txt", "a"))
sys.exit()


