mastercoin-vagrant
==================

Vagrant support for Mastercoin Development Environments.

[Vagrant](http://www.vagrantup.com) is a provisioning tool for creating virtual development environments. For a quick introduction to Vagrant and its potential benefits read [Why Vagrant?](http://docs.vagrantup.com/v2/why-vagrant/index.html)

The initial Vagrant file contains multiple VMs

base - used to make a base box for the other VMs (advanced users only)
empty - empty VM for quick tests of install from 'base'
tools - Mastercoin Tools
bitcoind-dev - A bitcoind VM (or can be mastercoind if you change the repo/branch)

uses the ```install-msc.sh``` script to install Mastercoin Tools. It pulls ```install-msc.sh``` directly from the [mastercoin-MSC/install-msc](https://github.com/mastercoin-MSC/install-msc) repository.

Prerequisites
-------------

* Virtual Box 4.3.10 or later
* Vagrant 1.5.3 or later

Vagrant is available for Mac OS X, Windows, and  Linux. In addition to VirtualBox, Vagrant may be used to provision VMWare, AWS and other virtual environments.

Base Box
--------

The Vagrantfile is currently using (*trusting*) the [parallels/ubuntu-13.10](https://vagrantcloud.com/parallels/ubuntu-13.10) base box created by Parallels and the Mastercoin base box [msgilligan/mastercoin-ubuntu-base](https://vagrantcloud.com/msgilligan/mastercoin-ubuntu-base).

You should consider them untrusted binaries. Only use them with TEST-MSC and samll amounts of Bitcoin.

Instructions
------------

1. [Install VirtualBox](https://www.virtualbox.org/manual/ch02.html)
1. [Install Vagrant](http://docs.vagrantup.com/v2/installation/)
1. Clone this repository

        git clone git@github.com:msgilligan/install-msc.git

1. Run Vagrant

        cd install-msc
        vagrant up

1. Connect to VirtualBox VM

        vagrant ssh tools

1. Go to the correct directory

        cd ~/mastercoin-tools/

1. Follow the instructions in the [Running](http://mastercoin-tools-installer.readthedocs.org/en/latest/pages/running.html) section of the install-msc documentation.

To Do
-----
1. Find the proper repo on Github to host Mastercoin Vagrant files

    That's install-msc I think.

1. Better documentation

    Coming soon

1. Track versions of all components used and update to released/stable versions asap.

    [versions.adoc](versions.adoc) os a startig point

1. Create a verified/trusted Mastercoin "base box"

    We have a mastercoin base box now, but it's not verified/trusted yet.

1. Vagrant file support for Omniwallet
1. Add [Shared folders and port-forwarding](http://pastie.org/9083315)
1. Vagrant file support for an Obelisk VM



Versions, tags, and hashes
--------------------------

I would like to see a 100% reproducible build/install. In order to do this all critical components should be versioned or tagged. I'm tracking versions of components in an AsciiDoc table named [versions.adoc](versions.adoc).
