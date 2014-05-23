mastercoin-vagrant
==================

Vagrant support for Mastercoin Development Environments.

[Vagrant](http://www.vagrantup.com) is a provisioning tool for creating virtual development environments. For a quick introduction to Vagrant and its potential benefits read [Why Vagrant?](http://docs.vagrantup.com/v2/why-vagrant/index.html)

The initial Vagrant file uses the ```install-msc.sh``` script to install Mastercoin Tools. It pulls ```install-msc.sh``` directly from the [mastercoin-MSC/install-msc](https://github.com/mastercoin-MSC/install-msc) repository.

Prerequisites
-------------

Initial testing of the Mastercoin Vagrant file has been done in the following environment:

* Mac OS X
* Virtual Box 4.3.10
* Vagrant 1.5.3

Vagrant is available for Mac OS X, Windows, and  Linux. In addition to VirtualBox, Vagrant may be used to provision VMWare, AWS and other virtual environments.

Base Box
--------

The Vagrantfile is currently using (*trusting*) the [parallels/ubuntu-13.10](https://vagrantcloud.com/parallels/ubuntu-13.10) base box created by Parallels.

Instructions
------------

1. [Install VirtualBox](https://www.virtualbox.org/manual/ch02.html)
1. [Install Vagrant](http://docs.vagrantup.com/v2/installation/)
1. Clone this repository

        git clone git@github.com:msgilligan/mastercoin-vagrant.git

1. Run Vagrant

        cd mastercoin-vagrant
        vagrant up

1. Connect to VirtualBox VM

        vagrant ssh

1. Follow the instructions in the [Running](http://mastercoin-tools-installer.readthedocs.org/en/latest/pages/running.html) section of the install-msc documentation.

To Do
-----
1. Find the proper repo on Github to host Mastercoin Vagrant files
1. Better documentation
1. Track versions of all components used and update to released/stable versions asap.
1. Create a verified/trusted Mastercoin "base box"
1. Vagrant file support for Omniwallet
1. Add [Shared folders and port-forwarding](http://pastie.org/9083315)
1. Vagrant file support for an Obelisk VM



Versions, tags, and hashes
--------------------------

I would like to see a 100% reproducible build/install. In order to do this all critical components should be versioned or tagged. I'm tracking versions of components in an AsciiDoc table named [versions.adoc](versions.adoc).
