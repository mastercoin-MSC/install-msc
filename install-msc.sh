#Outside Requirements: Existing Obelisk Server
#Instructions are for Ubuntu 13.04 and newer

#get the current directory

set -e
echo
echo " Mastercoin Tools Installation Script "
echo
if [ "$#" = "2" ]; then
    if [[ "$1" = "-os" ]]; then
        #Absolute path
        SERVER=$2
        PREFIG=CLE
    else
    	HELP=1
    fi
fi

if [ "$1" = "--help" ] || [ $HELP ]; then
     echo " [+] Install script help:"
     echo " --> To execute this script type:"
     echo " <sudo bash install-msc.sh>"
     echo " --> To execute this script and install with a specific obelisk server"
     echo " <bash install-msc.sh -os server-details:port>"
     echo " This script will install SX and the required prerequisites"
     echo " The SX install script will install libbitcoin, libwallet, obelisk and sx tools."
     echo " The standard path for the installation is /usr/local/"
     echo " The stardard path for the conf files is /etc."
     echo
     exit
fi

if [ `id -u` = "0" ]; then
    SRC=$PWD
else
    echo
    echo "[+] ERROR: This script must be run as root." 1>&2
    echo
    echo "<sudo bash install-msc.sh>"
    echo
    exit
fi


while [ -z "$PREFIG" ]; do
	echo "Do you have an obelisk server and wish to enter its details now? [y/n]"
	echo "Need an obelisk server? Try https://wiki.unsystem.net/index.php/Libbitcoin/Servers"
	read PREFIG
done

case $PREFIG in
	y* | Y* )
		ACTIVE=1
		CONFIRM=no
	;;

	CLE)
		ACTIVE=1
		CONFIRM=P
	;;

	*)
		active=0
	;;
esac

while [ $ACTIVE -ne 0 ]; do
	case $CONFIRM in

	y* | Y* )
		echo "Writing Details to ~/.sx.cfg"
		echo "You can update/change this file as needed later"
		echo "service = \""$SERVER"\"" > ~/.sx.cfg
		ACTIVE=0
	;;

	n* | N* )
		SERVER=
		while [ -z "$SERVER" ]; do
			echo "Enter Obelisk server connection details ex: tcp://162.243.29.201:9091"
			echo "If you don't have one yet enter anything, you can update/change this later"
			read SERVER
		done
		CONFIRM=P
	;;

	P)
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
sudo pip install -r pip.packages


cd $SRC/res
sudo bash install-sx.sh

cd
git clone https://github.com/grazcoin/mastercoin-tools.git
#git clone https://github.com/mastercoin-MSC/mastercoin-tools.git

cp $SRC/res/app.sh mastercoin-tools
cp $SRC/scripts/* mastercoin-tools

#update ~/.sx.cfg with an obelisk server details
# ~/.sx.cfg Sample file.
#service = "tcp://162.243.29.201:9091"

#add chown for the mastercoin-tools directory.

NAME=`logname`
sudo chown -R $NAME:$NAME mastercoin-tools

cd mastercoin-tools


echo ""
echo ""
echo "Installation complete"
echo "MSC-Tools should have been downloaded/installed in "$PWD
echo "A wrapper app has also been included which automates the following tasks"
echo ""
echo "------Manual Run Commands---------"
echo "To update with the latest transactions run: python msc_parse.py"
echo "To Validate and update address balances run: python msc_validate.py"
echo "Once thats done copy the results to the www directory"
echo "cp --no-clobber tx/* www/tx/"
echo "cp --no-clobber addr/* www/addr/"
echo "cp --no-clobber general/* www/general/"
echo "----------------------------------"
echo ""
echo "-----Automated Run Commands-------"
echo "start a new screen session with: screen -S msc-tools"
echo "cd "$SRC"/mastercoin-tools"
echo "launch the wrapper:  ./app.sh"
echo "you can disconnect from the screen session with <ctrl-a> d"
echo "----------------------------------"
