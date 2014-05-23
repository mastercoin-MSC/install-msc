#!/bin/sh
echo id is `id -u`
echo "Installing Git..."
apt-get -y install git
echo "Cloning install-msc.git..."
sudo -H -u vagrant git clone https://github.com/msgilligan/install-msc.git
cd install-msc
echo "Checkout out msgilligan-modularize branch"
sudo -H -u vagrant git checkout msgilligan-modularize
echo "Running install-prerequisites..."
bash install-prerequisites.sh


