#!/bin/bash
# Vagrant install script run as 'vagrant' user -- not sudo
echo "Running 'vagrant' user portion of install..."
cd /vagrant
echo "tcp://obelisk.bysh.me:9091" > $HOME/.sx.cfg OBELISK_SERVER
bash install-omni.sh 
