# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
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
      base.vm.box = "parallels/ubuntu-13.10"
      base.vm.provision "shell" do |s|
        s.path = "install-mastercoin-base-root.sh"
      end
  end

#
# empty
#
# Configuration for an empty install based on 'base'
#
  config.vm.define "empty" do |empty|
  end


#
# tools
#
# Configuration for a base Ubuntu VM for Mastercoin Tools
#
  config.vm.define "tools" do |tools|

      tools.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
      end

      tools.vm.provision "shell" do |s|
        s.path = "install-mastercoin-tools-root.sh"
    #    s.args = [$obeliskServerUrl]
      end

      tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-user.sh"
      end
  end


#
# bitcoind-dev
#
# Configuration for Bitcoind/Mastercoind development
#
  config.vm.define "bitcoind-dev", autostart: false do |bitcoind|
      bitcoind.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 4
      end

      bitcoind.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "clone-and-build-bitcoind.sh"
        s.args = ["https://github.com/msgilligan/bitcoin.git", "omniwallet-master", "bitcoin"]
      end

  end

end
