===============
Troubleshooting
===============

Having issues? Things not working as expected?

Here are a few 'Gotchyas' that we've encountered and what to check/how to fix them. 

Permissions
-----------

One of the first things to check is folder permissions. 
The installer tries to figure out what user is running the installer and set the permissions for the folders it creates appropriately. 
If this happens the user you run "app.sh" as may not have permission to access the necessary folders. 

Items to Check
^^^^^^^^^^^^^^

There are 2 main items that need their permissions checked:

* /var/lib/mastercoin-tools    # Data directory
* ~/mastercoin-tools           # Tools directory

Fix
^^^

These need to be owned by the user who is going to run "app.sh"::

 sudo chown -R <youruser>:<youruser> /var/lib/mastercoin-tools
 sudo chown -R <youruser>:<youruser> /home/<youruser>/mastercoin-tools


SX Settimgs
-----------

One of the other issues we've seen is the use of an Obelisk server that isn't responding properly. 

Items to Check
^^^^^^^^^^^^^^

* sx config file in the home directory of the user running "app.sh" 

::

 /home/<youruser>/.sx.cfg

* Check that the sx server is actually responding 

::

 sx fetch-last-height   #should return the block height number


Fix
^^^

* Make sure you are running "app.sh" as the user who has the sx config file in their home directory
* Try a different sx server. We have had decent experience using: *obelisk.bysh.me:9091*

