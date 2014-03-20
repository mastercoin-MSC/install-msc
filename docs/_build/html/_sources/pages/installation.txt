==================
Installation/Setup
==================

Prerequisites
-------------

The msc-tools leverage an existing obelisk server.
During installation the script will prompt you if you have one.
If not you can come back later and update your ~/.sx.cfg file with the correct details.

Need a server? Try checking `UN Systems wiki <https://wiki.unsystem.net/index.php/Obelisk/Servers>`_

Recommended System Requirements
---------------------------

* 12Gb+ Disk space
* 1 Gig+ Ram (Amazon base EC2 instance with 512 will fail to build)
* Use a Tested Environment

Tested Environments
-------------------

The installation utility and all components have been tested in the following environments:

* ubuntu-server-13.10 ( 32 | 64 )

Installing (auto)
-----------------

An installation script has been provided that automates the installation process.
It will prompt for obelisk server details and can be run with the following commands

::

    git clone https://github.com/achamely/install-msc.git  
    cd install-msc  
    sudo bash install-msc.sh

Optionally you can provide the obelisk server details on the cli

::

    sudo bash install-msc.sh -os tcp://your.obelisk.server.org:9091


Installing (manual)
-------------------

If you want to manually install all of the components you can do so with the following commands. 

::

    #Update the apt-get packages
    sudo apt-get update

    #install required supporting packages:
    sudo apt-get -y install git python-simplejson python-git python-pip
    sudo apt-get -y install make
    sudo apt-get -y install git build-essential autoconf libtool libboost-all-dev pkg-config libcurl4-openssl-dev libleveldb-dev libzmq-dev libconfig++-dev libncurses5-dev
    sudo pip install -r pip.packages

    #Install SX using the modified installation script
    #Note, this script installs specific revisions of the sx components known to work with mastercoin-tools
    sudo bash install-sx.sh

    #Download the mastercoin-tools
    git clone https://github.com/mastercoin-MSC/mastercoin-tools.git

    #copy the scripts and app.sh wrapper for mastercoin tools to the mastercoin-tools directory
    cp install-msc/res/app.sh mastercoin-tools/
    cp install-msc/scripts/* mastercoin-tools/

    #update ~/.sx.cfg with an obelisk server details
    # ~/.sx.cfg Sample file.
    #service = "tcp://162.243.29.201:9091"

    #Mastercoin-tools directory needs to have permissions set to the user who will run it
     sudo chown -R `logname`:`logname` mastercoin-tools

