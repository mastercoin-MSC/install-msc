#!/bin/bash
REPOURL=$1
BRANCH=$2
REPODIR=$3

# Should we install QT here or provide an option to do it?

git clone --no-checkout $REPOURL $REPODIR
cd $REPODIR
git checkout $BRANCH

# Build 

./autogen.sh
./configure
make

# Run


