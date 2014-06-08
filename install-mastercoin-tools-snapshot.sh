#!/bin/bash
# Vagrant install script run as 'vagrant' user -- not sudo
echo "Installing Mastercoin Tools transaction state snapshot..."
cd /var/lib/mastercoin-tools
7z x /vagrant/res/mtools-snapshot.7z
