#!/usr/bin/python
import json
import os
import time

def configure_hostapd(AP_info):
    target_ssid = str(AP_info['ssid'])
    print "[-] configuring hostapd . . ."
    with open('conf_files/hostapd.conf','w') as opened_file:
        opened_file.write('interface=wlan0mon\ndriver=nl80211\n')
        opened_file.write('ssid=%s\n' % (target_ssid))
        opened_file.write('hw_mode=g\nchannel=6\nmacaddr_acl=0\nignore_broadcast_ssid=0\n')
    time.sleep(15)
    print "[-] hostapd configured "




if __name__ == "__main__":
    try:                                                                                                          
        with open('ap_info_json/target_ap.json','r') as read_file:                                                
            json_obj = json.load(read_file)                                                                       
            configure_hostapd(json_obj)

    except Exception as e:
        print e
        print "[ERROR] something went wrong, can't locate target ap info."
        if int(os.system('ls ap_info_json/ -1q | wc -l')) <1:
            print "[ERROR] AP info file not found"

