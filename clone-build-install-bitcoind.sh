#!/bin/bash
REPOURL=$1
BRANCH=$2
REPODIR=$3

# Clone and checkout using passed (usually from Vagrant) parameters
git clone --no-checkout $REPOURL $REPODIR
cd $REPODIR
git checkout $BRANCH

# Build bitcoind (Master Core)

./autogen.sh
./configure
make

# Install as an Upstart service
sudo ./contrib/msc-ubuntu/install-mastercore-upstart.sh



