#!/bin/sh
echo "Running install-sx..."
cd /vagrant/res
bash install-sx.sh

mkdir /var/lib/mastercoin-tools
chown -R vagrant:vagrant /var/lib/mastercoin-tools


