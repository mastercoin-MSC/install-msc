#Outside Requirements: Existing Obelisk Server 
#Instructions are for Ubuntu 13.04 and newer

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

#install libsodium then clean up the install files
cd
git clone https://github.com/jedisct1/libsodium.git
cd libsodium
./autogen.sh
./configure && make check
sudo make install
sudo ldconfig
cd ..
#sudo rm -rf libsodium

#install czmq
cd
git clone https://github.com/zeromq/czmq.git
cd czmq
./autogen.sh
./configure && make check
sudo make install
sudo ldconfig
cd ..
#sudo rm -rf czmq

#install libzmq, required for czmqpp, then we can uninstall it as it conflicts with obelisk
cd
git clone https://github.com/zeromq/libzmq.git
cd libzmq
sh autogen.sh
./configure
make
make check
sudo make install
sudo ldconfig
cd
#sudo rm -rf libzmq


#install czmqpp
cd
git clone https://github.com/darkwallet/czmqpp.git
cd czmqpp/
autoreconf -i
./configure LIBS=-I/lib/i386-linux-gnu/
make
sudo make install
sudo ldconfig
cd 
#sudo rm -rf czmqpp/

cd
cd libzmq
sudo make uninstall

#tricky stuff since obelisk looks for libczmq++ and it's listed as libczmqpp
sudo cp /usr/local/lib/pkgconfig/libczmqpp.pc /usr/local/lib/pkgconfig/libczmq++.pc

export PKG_CONFIG_PATH="/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH"


#install sx:
cd 
git clone https://github.com/spesmilo/sx.git
cd sx
#git checkout abec160
git checkout a97f7be
#wget http://sx.dyne.org/install-sx.sh
sudo bash install-sx.sh

cd
git clone https://github.com/grazcoin/mastercoin-tools

#update ~/.sx.cfg with an obelisk server details
# ~/.sx.cfg Sample file.
#service = "tcp://162.243.29.201:9091"

cd mastercoin-tools
mkdir -p tx addr general
# to update with latest transactions:
python msc_parse.py
# validate and update addresses balance:
python msc_validate.py
# copy the results to www directory
cp --no-clobber tx/* www/tx/
cp --no-clobber addr/* www/addr/
cp --no-clobber general/* www/general/
