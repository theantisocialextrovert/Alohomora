# Alohomora
** *this project is purely for educational purpose* **
this tool can be used for cracking wifi password, the way it works is,
1. sniff the network for beacon packets and collect the info about the target ap, this is done with p_sniffer.py
2. once we have the info about the victim/target ap, we are going to capture the 4-way handshake,
for this I've used an active method, rather than waiting for the clients to reconnect, actively dauth packets are
sent to the target AP, this is done with dauth_attack.py script.
3. now that we have the handshake, the next step is to launch *Evil Twin* attack. which will basically make a fake
AP with the same ssid(name of the wifi AP) and simultaneously send deauth packets to the real AP.
4. once the client connects to our fake AP, whenever they'll try to access the internet, a login page will appear in the default 
browser, they'll have to enter the password of the real AP, and the entered password will be verified by using the 4-way handshake
that we had already captured.
