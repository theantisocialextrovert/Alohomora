#!/usr/bin/python
from scapy.all import *
from threading import Thread
import pandas
import time
import os

class packet_sniffer:

    interface    = "wlan0mon"
    networks     = None
    index        = 0 
    channel_flag = True
    display_flag = True
    network_info = []
    target_bssid = None
    target_ssid  = None
    target_index = None

    def __init__(self):
        # initialize the networks dataframe that will contain all access points nearby
        self.networks = pandas.DataFrame(columns=["BSSID", "SSID", "dBm_Signal", "Channel", "Crypto","INDEX"])
        # set the index BSSID (MAC address of the AP)
        self.networks.set_index("BSSID", inplace=True)
        print "[-] initializing. . . ."
    
    def change_channel(self):
        channel = 1
        while self.channel_flag:
            time.sleep(1)
            print "current channel = ",channel
            os.system('iwconfig %s channel %d' % (self.interface, channel))
            next_channel = int(random.random() * 14)
            print "next_channel = ",next_channel

            if next_channel != 0 and channel != next_channel:
                channel = next_channel
    def display_networks(self):
        while self.display_flag:
            os.system("clear")
            print "flag = ", self.networks.empty
            print(self.networks)
            print "\n\n[-] enter CTRL + C to stop sniffing\n"
            time.sleep(1)

    def sniffer_method(self, packet):
        if packet.haslayer(Dot11Beacon):
            # getting the MAC address of the network
            bssid = packet[Dot11].addr2
            # getting  the name of the network
            ssid = packet[Dot11Elt].info.decode()
            try:
                dbm_signal = packet.dBm_AntSignal
            except:
                dbm_signal = "N/A"
            
            stats = packet[Dot11Beacon].network_stats()
            # getting the channel of the AP
            channel = stats.get("channel")
            # gettng the crypto
            crypto = stats.get("crypto")
            if bssid not in self.network_info or len(self.network_info) == 0:
                self.index+=1
                self.networks.loc[bssid] = (ssid, dbm_signal, channel, crypto,self.index)
                self.network_info.append(bssid)
                print "added new network === ", self.network_info

    def configure_hostpad(self):
        os.system("rm /conf/temp.conf")
        with open("temp.conf",'w') as hostpad_conf:
            hostpad_conf.write("interface=wlan0mon\n")
            hostpad_conf.write("driver=nl80211\n")
            hostpad_conf.write("ssid=temp\n")


    def start(self):
        # configuring the timeout timer for  sniffer
        print "[-] enter timeperiod for sniffing(in secs)\n[->] ",
        timeout_time = int(raw_input())
        print "\n[-] sniffing for ",timeout_time," sec. . ." 
        time.sleep(2)
        # starting the thread that prints all the networks
        printer = Thread(target=self.display_networks)
        printer.setDaemon(True)
        print "[-] starting display_networks deamon "
        printer.start()
        
        # starting the channel changer
        channel_changer = Thread(target=self.change_channel)
        channel_changer.setDaemon(True)
        print "[-] starting change_channel deamon"
        channel_changer.start()
        
        # configuring and starting the sniffer
        sniff(prn=self.sniffer_method, iface="wlan0mon", monitor=True, timeout = timeout_time)
        
        # flags to stop the display and channel deamons
        self.channel_flag = False
        self.display_flag = False

        # selecting the target ap from the available APs
        index        = int(raw_input("[-] enter the index of victim AP\n"))
        self.target_ssid  = self.networks.iloc[index-1]['SSID']
        print "df == == == ", self.networks.iloc[index-1]       
        self.target_bssid = self.network_info[index-1]
        print "targetbssid == ",self.target_bssid, " target_ssid = ",self.target_ssid
        
     
if __name__ == "__main__":
    temp = packet_sniffer()
    temp.start()
    
