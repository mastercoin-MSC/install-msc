=======
Running
=======

Included with mastercoin-tools are 2 different methods for downloading/updating the blockchain information.


app.sh
------
Continuous running application that you can start in a screen session. 
It will download/process the entire block chain and then sleep for 60 secs before checking for updates.::

    screen -S msc
    ./app.sh
    ctrl+a , d  <disconnect screen>

    reconnect at anytime with
    screen -r msc



msc_cron.sh
-----------

Alternatively you can schedule a cron job to execute the msc_cron.sh utility at your predetermined time. 
