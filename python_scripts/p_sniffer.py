#!/usr/bin/python
from scapy.all import *
from threading import Thread
import pandas
import time
import json
import os

class packet_sniffer:

    interface    = "wlan0mon"
    networks     = None
    index        = 0 
    channel_flag = True
    display_flag = True
    ap_list      = []
    target_ap_info={}

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
            os.system('iwconfig %s channel %d' % (self.interface, channel))
            next_channel = int(random.random() * 14)

            if next_channel != 0 and channel != next_channel:
                channel = next_channel
    
    def display_networks(self):
        while self.display_flag:
            os.system("clear")
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
            if bssid not in self.ap_list or len(self.ap_list) == 0:
                self.index+=1
                self.networks.loc[bssid] = (ssid, dbm_signal, channel, crypto,self.index)
                self.ap_list.append(bssid)

    def store_targetAP_info(self):
        with open("ap_info_json/target_ap.json",'w') as outfile:
            json.dump(self.target_ap_info, outfile)


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
        time.sleep(2)
        
        if self.networks.empty:
            print "[!!] No AP detected, exiting. . ."
            return
        # selecting the target ap from the available APs
        index = None
        while True:
            index        = int(raw_input("[-] enter the index of victim AP\n[->] "))
            if index > len(self.ap_list) or index <= 0:
                print "\n[ERROR] wrong input, enter again\n"
            else:
                break
        
        # extrating and storing the AP info into json
        target_ssid    = self.networks.iloc[index-1]['SSID']
        target_bssid   = self.ap_list[index-1]
        target_channel = self.networks.iloc[index-1]['Channel']

        print "[-] target AP's bssid: ",target_bssid, "\n[-] target AP's ssid : ",target_ssid
        self.target_ap_info['bssid']   = target_bssid
        self.target_ap_info['ssid']    = target_ssid
        self.target_ap_info['channel'] = target_channel
        self.target_ap_info['index']   = index
        self.store_targetAP_info()
        
     
if __name__ == "__main__":
    temp = packet_sniffer()
    temp.start()
    
