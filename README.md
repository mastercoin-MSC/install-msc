msc-install
===========

### Automated installation script for msc-tools and necessary components

This script automates the process of downloading and installing msc-tools package, sx and the required dependancies. 

###Prerequisites: 
 The msc-tools leverage an existing obelisk server.  
 During installation the script will prompt you if you have one.  
 If not you can come back later and update your ~/.sx.cfg file with the correct details.  

###Tested Environments
 ubuntu-server-13.10 ( 32 | 64 )

###To install:
```
git clone https://github.com/achamely/install-msc.git  
cd install-msc  
sudo bash install-msc.sh
```
(will prompt for obelisk server)  
 
Optionally you can provide the obelisk server details on the cli  
```
sudo bash install-msc.sh -os tcp://your.obelisk.server.org:9091
```
