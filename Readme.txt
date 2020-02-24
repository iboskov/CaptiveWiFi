ZeroFi has been
tested with the Raspberry Pi B+, Raspberry Pi 3, and Raspberry Pi Zero W.


BEFORE INITIAL INSTALLATION:
== Run "apt install python3 python3-pip dnsmasq hostapd -y" and "pip3 install flask"
== In /home/logatec/ create the script initial.sh and give chmod +x privileges
== In /etc/systemd/system/ create the initialboot.service


 SCRIPT-BASED INSTALLATION INSTRUCTIONS:

== Navigate to the directory where you downloaded or cloned ZeroFi

== Run:

sudo python3 initial_setup.py

CONFIGURATION:

== All of these variables can be set at any time after the Initial Setup has
been running by editing the /etc/zerofi/zerofi.conf

RESETTING THE DEVICE:

== You can also reset the device by running the manual_reset.py in the
/usr/lib/zerofi/reset_device directory as root or with sudo.
