#!/bin/bash

export fileText='ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=PL

network={
 ssid="'${1}'"
 psk="'${2}'"
}'

echo "$fileText" > /etc/wpa_supplicant/wpa_supplicant.conf
