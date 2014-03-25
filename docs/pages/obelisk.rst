=======
Obelisk
=======
.. _obelisk:

Some Information and Instructions taken from `Libbitcoin Obelisk Quickstart <http://libbitcoin.dyne.org/obelisk-setup.html>`_

What is Obelisk
---------------

Obelisk is a scalable blockchain query infrastructure which allows you to maintain your own copies of the blockchain for parsing/data interaction.  
Mastercoin tools needs/uses an obelisk server to query the blockchain and create/parse Mastercoin Transactions.  
There are some public obelisk servers available already on the `web <https://wiki.unsystem.net/index.php/Obelisk/Servers>`_, however if you wish 
to run your own server in house this guide will help you get started.  
For the purposes of this document there are three relevant parts: :ref:`server` , :ref:`workers`, and :ref:`clients`.

Installation
------------

By default Obelisk is installed when you run the Mastercoin-tools installer.
It is part of the :ref:`sx dependencies/installation package <installed_items>`. 

Configuration
-------------

The default Obelisk Configuration files are stored in ::

 /etc/obelisk


There are two files

* balancer.cfg
* worker.cfg


balancer.cfg
^^^^^^^^^^^^

.. _config:

Allows you to configure the port clients and workers will connect to:

* The default port for clients is `9091`.
* The default port for workers is `9092`.

You may modify these to suit your environment or leave them alone.

worker.cfg
^^^^^^^^^^

Contains all the information a obelisk workers needs to connect/respond to an obelisk server.  
The default settings should work just fine for a normal installation.  
If you have changed the 'client port' in the balancer.cfg or you are running obelisk workers on seperate machines you will need to update
the *service = "tcp://localhost:9092"*  with your updated/relevant details. 

.. _server:

Server
------

The obelisk server is what handles the interaction between the client requests and the workers response.  
It's entire operation is run by *obbalancer*  which uses the *balancer.cfg*  configuration to listen for workers and clients.

There are two methods for running the server. Screen or Daemon. 

Screen
^^^^^^

You can run the obbalancer in a screen session. This is easy to get started but may not be the most robust method.::

 screen -S obbalancer
 obbalancer

Disconnect from the screen session with::

 CTRL+A  D

You can reattach to the screen session with::

 screen -r obbalancer

to check on it's progress/status

Daemon
^^^^^^

The obelisk source includes an init.d script you can use.  
It is located in the *<install-src>/obelisk-git/scripts/init.d/*  directory.  
On a default installation this should be ::

 /usr/local/src/obelisk-git/scripts/init.d/obbalancer

You will need to copy the *obbalancer*  script to your /etc/init.d/ directory and set its permissions for executing::

 sudo cp /usr/local/src/obelisk-git/scripts/init.d/obbalancer /etc/init.d/
 sudo chmod 755 /etc/init.d/obbalancer

The obbalancer init.d script uses the username *ob*.  
If it doesn't exist create a limited permissions user with this name or update the script with the username you wish it to user::

 DAEMON_USER=ob

Once the script is setup you can start it with */etc/init.d/obbalancer start*.  
If you wish the script to start on system startup you can also run *update-rc.d obbalancer defauls*

.. _workers:

Workers
-------

These are the workhorses of the obelisk server. Each server leverages one or more connected workers to query the blockchain information they have.  
You can run multiple workers on the same machine or spread them out and run them from multiple machines for redundancy. Each worker uses/maintains
it's own copy of the block chain database.


Initial-Setup
^^^^^^^^^^^^^

*Note: Workers CAN NOT share the same data directories.*  
Each worker needs it's own directory to store it's files/information.

Create and initialize a blockchain database for each worker ::

  mkdir worker.1/
  cd worker.1/
  mkdir blockchain/
  sx initchain blockchain/
    
Bootstraping Data
^^^^^^^^^^^^^^^^^

If you have a bitcoind bootstrap.dat, then you can bootstrap a blockchain.  
See /usr/local/libbitcoin/tools/ (run 'sudo make' and see the bootstrap tool).

Alternatively, once 1 worker is up and running/fully synced, you can:

* Stop that workers 'obworker'
* copy the blockchain/ directory to the new workers directory
* start the original worker and then the new worker.

Running
^^^^^^^

Once the worker has been setup. You can start it using obworker.  
It is recommended that workers be run in a screen session for unattendted operation ::

 cd worker.1/
 screen -S worker.1
 obworker

You can detach from the screen session with::
 
 CTRL+A D  

You can also reattach to the screen to check on the status with::

 screen -r worker.1

Repeat this process for each worker you wish to start. 

Press CTRL-C and wait if you want to stop the worker.

You can see the output using 'tail -f debug.log' in each workers directory.

*Tip: Running multiple workers is good for redundancy in case one crashes or has problems.*

.. _clients:

Clients
-------

The client is who/what is actually requesting the information.  
In Mastercoin tools the client is the local installation of sx which queries the obelisk server for blockchain information.  
Clients can connect to an obelisk server on the :ref:`configured port <config>`.  
For proper operation the Obelisk server should be setup, running, and have fully syned workers connected to it. 

If you are using a local installation of the obelisk server make sure to update the sx configuration file ::

 ~/.sx.cfg

Run a few test commands with sx to confirm operation ::

 sx fetch-last-height     :Returns current height the obelisk server knows

or ::

 sx balance <btc address>    :Returns balance in satoshis


