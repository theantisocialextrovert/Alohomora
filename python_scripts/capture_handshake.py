#!/usr/bin/python

import os
import json

def capture_handshake(AP_info):
    target_bssid   = str(AP_info['bssid'])
    target_channel = int(AP_info['channel'])
    os.system('airodump-ng wlan0mon --bssid %s --channel %d --write handshake --output-format cap' % (target_bssid,target_channel))

if __name__ == "__main__":
    try:
        with open('ap_info_json/target_ap.json','r') as read_file:
            json_obj = json.load(read_file)
            capture_handshake(json_obj)
    except:
        print "[ERROR] something went wrong, can't locate target ap info."
        print os.system('ls ap_info_json/ -1q | wc -l')

