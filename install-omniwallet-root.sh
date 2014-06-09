#!/bin/sh
MSC_USER=$1
MSC_GROUP=$2
echo "Running install-sx..."
cd /vagrant/res
bash install-sx.sh

mkdir /var/lib/mastercoin-tools
chown -R $MSC_USER:$MSC_GROUP /var/lib/mastercoin-tools


