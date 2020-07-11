#!/bin/bash
printf "[-] instaling hostapd. . .\n"
apt-get install hostapd 
printf "[-] instaling dnsmasq. . .\n"
apt-get install dnsmasq 
printf "[-] instaling apache2. . .\n"
apt-get install apache2
printf "[-] instaling toilet. . .\n"
apt-get install toilet
printf "[-] instaling xterm. . .\n"
apt-get install xterm
printf "[-] instaling dsniff. . .\n"
apt-get install dsniff
printf "[-] instaling scapy. . .\n"
pip install scapy
