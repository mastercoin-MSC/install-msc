# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  # Every Vagrant virtual environment requires a box to build off of.
  # Version 0.2.0 is Ubuntu 14.04 LTS built from "ubuntu/trusty64"
  config.vm.box = "msgilligan/mastercoin-ubuntu-base"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 2
    #v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"] #limit the use of cpu to 50%
  end

  config.vm.provider :aws do |aws, override|
    aws.access_key_id = ENV['AWS_ACCESS_KEY'] || ""
    aws.secret_access_key = ENV['AWS_SECRET_KEY'] || ""
    aws.keypair_name = ENV['AWS_KEYPAIR_NAME'] || ""

    aws.region = "us-west-1"
    aws.instance_type = "m1.small"
    aws.security_groups =  [ 'vagrant' ]

# ubuntu/images/ebs/ubuntu-trusty-14.04-amd64-server-20140607.1 - ami-a26265e7
# ebs, paravirtualization, 64-bit
# uswest-1
    aws.ami = "ami-a26265e7"

    override.vm.box = "mitchellh-dummy-aws"
    override.ssh.username = "ubuntu"
    override.ssh.private_key_path = ENV['AWS_SSH_KEY_PATH'] || ""
  end

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

#
# Use echo-params.sh to demonstrate provisioning script overrides.
#

    empty.vm.provision "shell" do |s|
      s.path = "echo-params.sh"
      s.args = [ "script", "1" ]
    end

    empty.vm.provision "shell", id: "script2"  do |s|
      s.path = "echo-params.sh"
      s.args = [ "script", "2" ]
    end

    empty.vm.provider :aws do |aws, override|
      aws.instance_type = "t1.micro"
      override.vm.provision "shell", id: "script2" do |s|
        s.args = [ "script", "2", "with modified params" ] 
      end
    end

  end


#
# tools
#
# Configuration for Ubuntu VM with Mastercoin Tools
#
  config.vm.define "tools" do |tools|

#      tools.vm.network :forwarded_port, guest: 22, host: 2223

      tools.vm.provision "shell" do |s|
        s.path = "install-mastercoin-base-root.sh"
      end

      tools.vm.provision "shell", id: "sh-tools-root" do |s|
        s.path = "install-mastercoin-tools-root.sh"
        s.args = [ "vagrant", "vagrant" ]   # user, group for /var/lib/mastercoin-tools
      end

      tools.vm.provider :aws do |aws, override|
        override.vm.provision "shell", id: "sh-tools-root" do |s|
          s.args = [ "ubuntu", "ubuntu" ]   # user, group for /var/lib/mastercoin-tools
        end
      end

     tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-user.sh"
      end

     tools.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-mastercoin-tools-snapshot.sh"
      end

      tools.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
      end
  end


#
# omni
#
# Configuration for Ubuntu VM with Omniwallet
#
  config.vm.define "omni" do |omni|

    omni.vm.network :forwarded_port, host_ip: "127.0.0.1", guest: 80, host: 1666

      omni.vm.provider "virtualbox" do |v|
        v.memory = 1024
        v.cpus = 2
      end

      omni.vm.provision "shell", id: "sh-omni-root" do |s|
        s.path = "install-omniwallet-root.sh"
        s.args = [ "vagrant", "vagrant" ]   # user, group for /var/lib/omniwallet
      end 

      omni.vm.provider :aws do |aws, override|
        override.vm.provision "shell", id: "sh-omni-root" do |s|
          s.args = [ "ubuntu", "ubuntu" ]   # user, group for /var/lib/omniwallet
        end
      end

      omni.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "install-omniwallet-user.sh"
      end

  end

#
# mastercore
#
# Configuration for Mastercore development
#
  config.vm.define "mastercore", autostart: false do |mastercore|

#    mastercore.vm.network :forwarded_port, guest: 22, host: 2230
    mastercore.vm.network :forwarded_port, host_ip: "127.0.0.1", guest: 8332, host: 28332
 
    mastercore.vm.provision "shell" do |s|
      s.path = "install-mastercoin-base-root.sh"
    end

    mastercore.vm.provision "shell" do |s|
        s.privileged = false
        s.path = "clone-build-install-bitcoind.sh"
        s.args = ["https://github.com/msgilligan/mastercore.git", "msgilligan-msc-upstart", "mastercore"]
    end

    mastercore.vm.provider "virtualbox" do |v|
        v.memory = 2048
        v.cpus = 8
    end

  end

end
