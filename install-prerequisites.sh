#!/bin/bash
sudo apt-get update

#install packages:
sudo apt-get -y install python-simplejson python-git python-pip
sudo apt-get -y install git curl p7zip-full make
sudo apt-get -y install build-essential autoconf libtool libboost-all-dev pkg-config libcurl4-openssl-dev libleveldb-dev libzmq-dev libconfig++-dev libncurses5-dev
sudo pip install -r pip.packages
