Mastercoin Vagrant
==================

Vagrant support for Mastercoin Development Environments.

[Vagrant](http://www.vagrantup.com) is a provisioning tool for creating virtual development environments. For a quick introduction to Vagrant and its potential benefits read [Why Vagrant?](http://docs.vagrantup.com/v2/why-vagrant/index.html)

The initial Vagrant file contains multiple VMs

* base - used to make a base box for the other VMs (advanced users only)
* empty - empty VM for quick tests of install from 'base'
* tools - Mastercoin Tools
* mastercore-dev - A mastercore VM (built from latest dev version)

uses the ```install-msc.sh``` script to install Mastercoin Tools.

Prerequisites
-------------

* Virtual Box 4.3.10 or later
* Vagrant 1.6.2 or later

Vagrant is available for Mac OS X, Windows, and  Linux. In addition to VirtualBox, Vagrant may be used to provision VMWare, AWS and other virtual environments.

Base Box
--------

The [Vagrantfile](Vagrantfile) is currently using (*trusting*) the [ubuntu/trusty64](https://vagrantcloud.com/ubuntu/trusty64) base box created by Ubuntu and the Mastercoin base box [msgilligan/mastercoin-ubuntu-base](https://vagrantcloud.com/msgilligan/mastercoin-ubuntu-base).

You should consider them untrusted binaries. Only use them with TEST-MSC and small amounts of Bitcoin.

Installing Mastercoin Tools
---------------------------

The ```tools``` VM is configured to install Mastercoin Tools.

1. [Install VirtualBox](https://www.virtualbox.org/manual/ch02.html)
1. [Install Vagrant](http://docs.vagrantup.com/v2/installation/)
1. Clone this repository and check out the 'vagrant' branch

        git clone git@github.com:mastercoin-MSC/install-msc.git
        cd install-msc
        git checkout vagrant

1. Run Vagrant

        vagrant up tools

1. Connect to VirtualBox VM

        vagrant ssh tools

1. Go to the correct directory

        cd ~/mastercoin-tools/

1. Follow the instructions in the [Running](http://mastercoin-tools-installer.readthedocs.org/en/latest/pages/running.html) section of the install-msc documentation.

Installing Mastercore
---------------------

The ```mastercore-dev``` VM is configured to install Mastercore.

1. [Install VirtualBox](https://www.virtualbox.org/manual/ch02.html)
1. [Install Vagrant](http://docs.vagrantup.com/v2/installation/)
1. Clone this repository and check out the 'vagrant' branch

        git clone git@github.com:mastercoin-MSC/install-msc.git
        cd install-msc
        git checkout vagrant

1. Run Vagrant

        vagrant up  mastercore-dev

1. Connect to VirtualBox VM

        vagrant ssh  mastercore-dev

1. Go to the mastercore build directory

        cd mastercore

1. Run the unit tests

        ./src/test/test_bitcoin
The unit tests will generate about a dozen screens of output and, if successful, the last line should read:

        *** No errors detected

1. Congratulations you have built and tested Mastercore!


AWS Installation
----------------

We now have experimental AWS support for Mastercoin Tools. Currently it is in a new VM called `tools-aws`. Before using the Vagrant AWS provider you'll need to install it:

    vagrant plugin install vagrant-aws

We use a "dummy" AWS base box [as recommended](https://github.com/mitchellh/vagrant-aws#quick-start) by mitchellh in the `vagrant-aws` README. This is a small text file that simply specifies that the base box is an AWS image, but leaves the specification of the actual base AMI image to the `Vagrantfile` itself. Use the following command to install the "dummy" box:

    vagrant box add mitchellh-dummy-aws https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box

You'll also need to configure your private AWS information by creating a *private* shell script:

    cp setup-aws-template.sh setup-aws-private.sh
    chmod 700 setup-aws-private.sh

Edit `setup-aws-private.sh` and enter your AWS information.

VM Installation is the same as for the Virtual Box version of Mastercoin Tools with the `vagrant up` command changed to:

    source setup-aws-private.sh
    vagrant up tools-aws --provider=aws
    source unset-aws-private.sh

and the `vagrant ssh` command changed to:

    source setup-aws-private.sh
    vagrant ssh tools-aws
    source unset-aws-private.sh

Don't forget to source the `unset-aws-private.sh` to remove your private information from environment variables.

To Do
-----

1. Better documentation

    Coming soon

1. Track versions of all components used and update to released/stable versions asap.

    [versions.adoc](versions.adoc) as a starting point

1. Create a verified/trusted Mastercoin "base box"

    We have a mastercoin base box now, but it's not verified/trusted yet.

1. Vagrant file support for Omniwallet
1. Add [Shared folders and port-forwarding](http://pastie.org/9083315)
1. AWS Instance configurations

    Using the [AWS Provider](https://github.com/mitchellh/vagrant-aws).



Versions, tags, and hashes
--------------------------

I would like to see a 100% reproducible build/install. In order to do this all critical components should be versioned or tagged. I'm tracking versions of components in an AsciiDoc table named [versions.adoc](versions.adoc).
