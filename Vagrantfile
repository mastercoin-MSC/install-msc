# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  # Version 0.2.0 is Ubuntu 14.04 LTS built from "ubuntu/trusty64"
  config.vm.box = "msgilligan/mastercoin-ubuntu-base"


#
# base
#
# Configuration for a base Ubuntu VM for Mastercoin
#
# Updated Ubuntu, make, git, libboost, etc
# See install-mastercoin-base-root.sh for details
#
# This VM is published on https://vagrantcloud.com as
# 'msgilligan/mastercoin-ubuntu-base' and used as the
# base box by all other VMs in this Vagrantfile.
# 
  config.vm.define "base", autostart: false do |base|
      base.vm.box = "ubuntu/trusty64"
      base.vm.provision "shell" do |s|
        s.path = "install-mastercoin-base-root.sh"
      end
  end

#
# empty
#
# Configuration for an empty install based on 'base'
#
  config.vm.define "empty", autostart: false  do |empty|
  end


#
# tools
#
# Configuration for Ubuntu VM with Mastercoin Tools
#
  config.vm.define "tools" do |tools|

#      tools.vm.network :forwarded_port, guest: 22, host: 2223

      tools.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
      end

      tools.vm.provision "shell" do |s|
        s.path = "install-mastercoin-tools-root.sh"
        s.args = [ "vagrant", "vagrant" ]   # user, group for /var/lib/mastercoin-tools
      end

      tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-user.sh"
      end

      tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-snapshot.sh"
      end

  end

#
# tools-aws
#
# Configuration for Ubuntu VM with Mastercoin Tools
#
# With a little tweaking this can be combined with tools
# and switched via provider, but this is a first cut
#
#

  config.vm.define "tools-aws" do |tools|
      tools.vm.box = "mitchellh-dummy-aws"

      tools.vm.provision "shell" do |s|
        s.path = "install-mastercoin-base-root.sh"
      end

      tools.vm.provision "shell" do |s|
        s.path = "install-mastercoin-tools-root.sh"
        s.args = [ "ubuntu", "ubuntu" ]   # user, group for /var/lib/mastercoin-tools
      end

      tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-user.sh"
      end

      tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-snapshot.sh"
      end


    tools.vm.provider :aws do |aws, override|
      aws.access_key_id = ENV['AWS_ACCESS_KEY']
      aws.secret_access_key = ENV['AWS_SECRET_KEY']
      aws.keypair_name = ENV['AWS_KEYPAIR_NAME']

      aws.region = "us-west-1"
      aws.instance_type = "m1.small"
      aws.security_groups =  [ 'vagrant' ]

  # ubuntu/images/ebs/ubuntu-trusty-14.04-amd64-server-20140607.1 - ami-a26265e7
  # ebs, paravirtualization, 64-bit
  # uswest-1
      aws.ami = "ami-a26265e7"

      override.ssh.username = "ubuntu"
      override.ssh.private_key_path = ENV['AWS_SSH_KEY_PATH']
    end

  end

#
# omni
#
# Configuration for Ubuntu VM with Omniwallet
#
  config.vm.define "omni" do |omni|

      omni.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
      end

      omni.vm.provision "shell" do |s|
        s.path = "install-omniwallet-root.sh"
        s.args = [ "vagrant", "vagrant" ]   # user, group for /var/lib/mastercoin-tools
      end

      omni.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-omniwallet-user.sh"
      end

  end

#
# mastercore-dev
#
# Configuration for Mastercore development
#
  config.vm.define "mastercore-dev", autostart: false do |mastercore|

#    mastercore.vm.network :forwarded_port, guest: 22, host: 2230
    mastercore.vm.network :forwarded_port, host_ip: "127.0.0.1", guest: 18332, host: 28332
 
    mastercore.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 8
    end

    mastercore.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "clone-and-build-bitcoind.sh"
        s.args = ["https://github.com/m21/mastercore.git", "new_m13", "mastercore"]
    end

  end

end
