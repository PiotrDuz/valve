#!/bin/bash
# REMEMBER TO ENABLE i2c manually !
# username is: dzawor
sudo apt-get update
sudo apt-get -y install python3
#git clone https://github.com/PiotrDuz/valve.git
python3 -m venv new_venv
new_venv/bin/pip install -r valve/requirements.txt
echo 'setup files'
chmod +x valve/restartValve.sh
sudo mv valve/restartValve.sh /usr/sbin
chmod +x valve/setWifi.sh
sudo mv valve/setWifi.sh /usr/sbin
chmod +x valve/startAP.sh
sudo mv valve/startAP.sh /usr/sbin
sudo echo 'dzawor ALL=(ALL) NOPASSWD: /usr/sbin/setWifi.sh' >> /etc/sudoers
sudo echo 'dzawor ALL=(ALL) NOPASSWD: /usr/sbin/restartValve.sh' >> /etc/sudoers
sudo echo 'dzawor ALL=(ALL) NOPASSWD: /usr/sbin/startAP.sh' >> /etc/sudoers
#sudo apt-get install apache2-utils rotate logs not needed
chmod +x valve/launch.sh
echo "
[Unit]
Description=dzawor service
[Service]
Type=simple
Restart=always
RestartSec=2
StandardOutput=append:/home/dzawor/logs.txt
StandardError=append:/home/dzawor/logs.txt
ExecStartPre=find /home/dzawor/logs.txt -size +100M -delete
User=dzawor
ExecStart=/home/dzawor/new_venv/bin/python /home/dzawor/valve/main.py
[Install]
WantedBy=multi-user.target
" > /etc/systemd/system/dzawor.service
#systemctl enable dzawor