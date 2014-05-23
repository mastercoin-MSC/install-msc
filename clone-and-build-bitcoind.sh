#!/bin/bash
REPOURL=$1
BRANCH=$2
REPODIR=$3

echo Installing packages needed to build bitcoind/mastercoind...

sudo apt-get install libssl-dev
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:bitcoin/bitcoin
sudo apt-get update
sudo apt-get install libdb4.8-dev
sudo apt-get install libdb4.8++-dev

# Should we install QT here or provide an option to do it?

git clone --no-checkout $REPOURL $REPODIR
cd $REPODIR
git checkout $BRANCH

# Build 

./autogen.sh
./configure
make

# Run


