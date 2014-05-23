#!/bin/bash
# Vagrant install script run as 'vagrant' user -- not sudo
echo "Running 'vagrant' user portion of install..."
cd install-msc
OBELISK_SERVER="tcp://obelisk.bysh.me:9091"
bash install-msc.sh -autoskipprereq $OBELISK_SERVER
