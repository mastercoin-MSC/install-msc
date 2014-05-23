#!/bin/sh
echo "Cloning install-msc.git..."
sudo -H -u vagrant git clone https://github.com/msgilligan/install-msc.git
cd install-msc
echo "Checkout out msgilligan-modularize branch"
sudo -H -u vagrant git checkout msgilligan-modularize
echo "Running install-sx..."
cd res
bash install-sx.sh

mkdir /var/lib/mastercoin-tools
chown -R vagrant:vagrant /var/lib/mastercoin-tools


