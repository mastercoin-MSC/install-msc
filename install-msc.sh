#Outside Requirements: Existing Obelisk Server 
#Instructions are for Ubuntu 13.04 and newer

#get the current directory
SRC=`pwd`

echo $SRC

while [ -z "$PREFIG" ]; do 
	echo "Do you have an obelisk server and wish to enter its details now? [y/n]"
	read PREFIG
done

case $PREFIG in
	y* | Y* )
		active=1
		CONFIRM=no	
	;;	
	*)
		active=0
	;;
esac

while [ $active -ne 0 ]; do
	case $CONFIRM in

	y* | Y* )
		echo "Writing Details to ~/.sx.cfg"
		echo "You can update/change this file as needed later"
		echo "service = \""$SERVER"\"" > ~/.sx.cfg
		active=0
	;;
	
	n* | N* )
		SERVER=
		while [ -z "$SERVER" ]; do  
			echo "Enter Obelisk server connection details ex: tcp://162.243.29.201:9091"
			echo "If you don't have one yet enter anything, you can update/change this later"
			read SERVER
		done

		echo "You entered: "$SERVER
		echo "Is this correct? [y/n]"
		read CONFIRM			
	;;
	
	*)
		CONFIRM=no
	;;
	esac
done

sudo apt-get update

#install packages:
sudo apt-get -y install git python-simplejson python-git python-pip
sudo apt-get -y install make
sudo apt-get -y install git build-essential autoconf libtool libboost-all-dev pkg-config libcurl4-openssl-dev libleveldb-dev libzmq-dev libconfig++-dev libncurses5-dev
sudo pip install ecdsa
sudo pip install pycoin

cd $SRC/sx
sudo bash install-sx.sh

cd
git clone https://github.com/grazcoin/mastercoin-tools

#update ~/.sx.cfg with an obelisk server details
# ~/.sx.cfg Sample file.
#service = "tcp://162.243.29.201:9091"

cd mastercoin-tools
mkdir -p tx addr general
# to update with latest transactions:
##python msc_parse.py
# validate and update addresses balance:
##python msc_validate.py
# copy the results to www directory
##cp --no-clobber tx/* www/tx/
##cp --no-clobber addr/* www/addr/
##cp --no-clobber general/* www/general/
