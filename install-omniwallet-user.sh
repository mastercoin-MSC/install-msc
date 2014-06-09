#!/bin/bash
# Vagrant install script run as 'vagrant' user -- not sudo
echo "Running 'vagrant' user portion of install..."
cd /vagrant
OBELISK_SERVER="tcp://obelisk.bysh.me:9091"
bash install-omni.sh -autoskipprereq $OBELISK_SERVER
