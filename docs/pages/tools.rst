=====
Tools
=====

List of tools included with the installation and how to use them

.. _msc_createtx:

msc_createtx.py
---------------

Purpose:
^^^^^^^^
Used to create, sign and/or send a Masterprotocol currency transaction

Checks:
^^^^^^^

Checks from address to make sure it has:

* Enough BTC to create/send the transaction
* Balance of the CurrencyID to make sure it has enough to send msc_send_amt

 * Balance is checked using 2 online resources (Masterchest.info and Omniwallet)

Inputs:
^^^^^^^
Takes json input via STDIN for the following variables:

* transaction_from: The Public Address of the Sender
* transaction_to: The Public address of the Receipiant
* currency_id: Currency ID to send. 1 for MSC, 2 for TMSC
* property_type: 1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)
* send_amt: The amount of the Currency ID to send
* from_private_key: Base58 Private Key of the sender's Public Address (Note: Should start with 5)``*``
* broadcast: Create, Sign and/or Broadcast Tx.

  * 0 - Create the Unsigned TX file only
  * 1 - Create and Sign the TX file 
  * 2 - Create, Sign and Broadcast the TX file

* clean: Clean up any of the tx files created.``*``

  * 0 - Keep all Tx files created
  * 1 - Remove only the intersigned Tx files. (Leaves the original unsigned Tx and the signed Tx)
  * 2 - Remove all unsigned Tx files. Will leave only the signed Tx file that can be broadcast to the network.
  * 3 - Remove all Tx files. Signed and unsigned, make sure you have broadcast the Tx before you do this.

*Note: ``*`` Only required if you are signing/broadcasting the tx file and can be omitted if just creating unsigned file.*

The json takes the following format::

        {
          "transaction_from": "{{Public from Address}}",
          "transaction_to": "{{Public to Address}}",
          "currency_id": {{1 for MSC, 2 for TMSC}},
          "send_amt": {{amount to send}},
          "property_type": {{1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)}}
          "broadcast": {{1 to create and broadcast or 0 to just create}},
          "from_private_key": "{{private key for signing}}",
          "clean": {{0 -keep all tx files, 1 -remove intersigned tx, 2 -remove all unsigned, 3 -remove all}}
        }

Ex:

*Note: for security the following was a brand new empty wallet. You should replace it's details with your own applicable info*::

        {
          "transaction_from": "1GGJMZoaxYMS4jsiLwPVbofe5YJyM6ER2i",
          "transaction_to": "19hf8QEkD3GR7NhUrujWXRg6e4gsHUTysp",
          "currency_id": 1,
          "send_amt": 5.1,
          "property_type": 2,
          "from_private_key": "5JXxd7qecXrzd9hJGdJsBnwkfJauHxVqbqRmBqQUjhrbGJPgoWb",
          "broadcast": 1,
          "clean": 1
        }

For reference, here is what the brainwallet.org generator page for the above address looks like.
Take note of the 'Uncompressed/Compressed' option

.. image:: brainwallet.uncompressed.png
    :align: center

Output:
^^^^^^^
Will return a json formated output.
Errors will be returned with json that contains ::

 {
    "status": "Status message",
    "error": "error details",
    "fix": "Corrective action to resolve the issue"
 }

Successful run will return json that contains::

 {
   "status": "Broadcast/Created/Signed status",
   "valid_check": "Validity check of signed file",
   "hash": "Hash of the tx",
   "st_file": "location/name of the signed tx file"
 }

Running:
^^^^^^^^
Standalone running/testing can be done by creating a json file (see input details or example_send.json for structure)
You can execute/run the program with::

 cat your_file.json | python msc_txcreate.py



msc-sxsend.py
-------------

Purpose:
^^^^^^^^
DEPRECIATED, Please see :ref:`msc_createtx.py <msc_createtx>`
Used to create (and/or send) a Mastercoin transaction

Checks:
^^^^^^^

Checks from address to make sure it has:

* Enough BTC to create/send the transaction
* Balance of the CurrencyID to make sure it has enough to send msc_send_amt

 * Balance is checked using the :ref:`msc-balance.py <msc-balance>` script

Inputs:
^^^^^^^
Takes json input via STDIN for the following variables:

* transaction_from: The Public Address of the Sender
* transaction_to: The Public address of the Receipiant
* currency_id: Currency ID to send. 1 for MSC, 2 for TMSC
* msc_send_amt: The amount of the Currency ID to send
* property_type: 1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)
* from_private_key: Base58 Private Key of the sender's Public Address (Note: Should start with 5)
* broadcast: Create and/or Broadcast Tx. 1 to create and broadcast or 0 to just create
* clean: Clean up any of the tx files created.

  * 0 - Keep all Tx files created
  * 1 - Remove only the intersigned Tx files. (Leaves the original unsigned Tx and the signed Tx)
  * 2 - Remove all unsigned Tx files. Will leave only the signed Tx file that can be broadcast to the network. 
  * 3 - Remove all Tx files. Signed and unsigned, make sure you have broadcast the Tx before you do this.



The json takes the following format::

	{
	  "transaction_from": "{{Public from Address}}",
	  "transaction_to": "{{Public to Address}}",
	  "currency_id": {{1 for MSC, 2 for TMSC}},
	  "msc_send_amt": {{amount to send}},
	  "property_type": {{1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)}}
	  "from_private_key": "{{private key for signing}}",
	  "broadcast": {{1 to create and broadcast or 0 to just create}},
          "clean": {{0 -keep all tx files, 1 -remove intersigned tx, 2 -remove all unsigned, 3 -remove all}}
	}

Ex:

*Note: for security the following was a brand new empty wallet. You should replace it's details with your own applicable info*::

	{
	  "transaction_from": "1GGJMZoaxYMS4jsiLwPVbofe5YJyM6ER2i",
	  "transaction_to": "19hf8QEkD3GR7NhUrujWXRg6e4gsHUTysp",
	  "currency_id": 1,
	  "msc_send_amt": 5.1,
	  "property_type": 2,
	  "from_private_key": "5JXxd7qecXrzd9hJGdJsBnwkfJauHxVqbqRmBqQUjhrbGJPgoWb",
	  "broadcast": 1,
          "clean": 1
	}

For reference, here is what the brainwallet.org generator page for the above address looks like.
Take note of the 'Uncompressed/Compressed' option 

.. image:: brainwallet.uncompressed.png
    :align: center

Output:
^^^^^^^
Will return a json formated output.
Errors will be returned with json that contains ::

 { 
    "status": "Status message", 
    "error": "error details", 
    "fix": "Corrective action to resolve the issue"
 }

Successful run will return json that contains::

 { 
   "status": "Broadcast/Created status", 
   "valid_check": "Validity check of signed file", 
   "hash": "Hash of the tx", 
   "st_file": "location/name of the signed tx file"
 }

Running:
^^^^^^^^
Standalone running/testing can be done by creating a json file (see input details or example_send.json for structure)
You can execute/run the program with::

 cat your_file.json | python msc_sxsend.py


msc-txcreate.py
---------------

Purpose:
^^^^^^^^
DEPRECIATED, Please see :ref:`msc_createtx.py <msc_createtx>`
Used to create an unsigned Mastercoin transaction

Checks:
^^^^^^^

Checks from address to make sure it has:

* Enough BTC to create/send the transaction
* Balance of the CurrencyID to make sure it has enough to send msc_send_amt

 * Balance is checked using the :ref:`msc-balance.py <msc-balance>` script

Inputs:
^^^^^^^
Takes json input via STDIN for the following variables:

* transaction_from: The Public Address of the Sender
* transaction_to: The Public address of the Receipiant
* currency_id: Currency ID to send. 1 for MSC, 2 for TMSC
* msc_send_amt: The amount of the Currency ID to send
* property_type: 1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)


The json takes the following format::

        {
          "transaction_from": "{{Public from Address}}",
          "transaction_to": "{{Public to Address}}",
          "currency_id": {{1 for MSC, 2 for TMSC}},
          "msc_send_amt": {{amount to send}},
	  "property_type": {{1 for indivisible currency, 2 for divisible (MSC/TMSC are 2, Maidsafecoins are 1)}}
        }

Ex:

*Note: for security the following was a brand new empty wallet. You should replace it's details with your own applicable info*::

        {
          "transaction_from": "1GGJMZoaxYMS4jsiLwPVbofe5YJyM6ER2i",
          "transaction_to": "19hf8QEkD3GR7NhUrujWXRg6e4gsHUTysp",
          "currency_id": 1,
          "msc_send_amt": 5.1
        }

Output:
^^^^^^^
Will return a json formated output.
Errors will be returned with json that contains ::

 {
    "status": "Status message",
    "error": "error details",
    "fix": "Corrective action to resolve the issue"
 }

Successful run will return json that contains::

 {
   "status": "Created status",
   "st_file": "location/name of the unsigned tx file"
 }

Running:
^^^^^^^^
Standalone running/testing can be done by creating a json file (see input details or example_send.json for structure)
You can execute/run the program with::

 cat your_file.json | python msc-txcreate.py


.. _msc-balance:

msc-balance.py
--------------

Purpose:
^^^^^^^^
Used to get the Mastercoin balance of an address

Requirements:
^^^^^^^^^^^^^
This script leverages the existing mastercoin tools parsed/validated output.
Mastercoin tools should be installed and fully updated with the Mastercoin Data in::

 /var/lib/mastercoin-tools/mastercoin_verify/addresses/

Checks:
^^^^^^^

Will check/return the date of the parsed date as listed in ::

 /var/lib/mastercoin-tools/www/revision.json


Inputs:
^^^^^^^
Takes json input via STDIN for the following variables:

* address: The address you want to check the balance for
* currency_id: The currency you want the balance for

  * 1 - Mastercoin
  * 2 - Test Mastercoins

The json takes the following format::

        {
          "address": "{{Address to check}}",
          "currency_id": {{1 for MSC, 2 for TMSC}}
        }

Ex: ::

        {
          "address": "1CMauYumpA7YG8i4cPod8FadRLK95HxSob",
          "currency_id": 1
	}


Output:
^^^^^^^
Will return a json formated output

Completed run will return json that contains::

 { 
   "address": "Address checked",
   "currency_id": "Currency checked",
   "balance": "Balance or error message",
   "balancetime": "Time in GMT human readable",
   "epochtime": "Balance Timestamp in GMT epoch"
 }

*Note: If the revision file or currency address files are missing the time is omitted and an error message is returned for balance.*

Running:
^^^^^^^^
Standalone running/testing can be done by creating a json file (see input details or example_balance.json for structure)
You can execute/run the program with::

 cat your_file.json | python msc-balance.py



getConsensusMSC.py
------------------

Purpose:
^^^^^^^^
Used to get the consensus of local installation with Online sites
*Note: The final consensus authority is defined by the mastercoin tools code result.*
`Masterchain Consensus Report <https://masterchain.info/general/MSC-difference.txt>`_


Requirements:
^^^^^^^^^^^^^
This script leverages the existing mastercoin tools parsed/validated output.
Mastercoin tools should be installed and fully updated with the Mastercoin Data in::

 /var/lib/mastercoin-tools/mastercoin_verify/addresses/

Inputs:
^^^^^^^
Takes json input via STDIN for the sites you wish to validate consensus against:
*Note: At present generates consensus output for Currency ID 1 (MSC) only.* 

* site: The sites to compare local results against


The json takes the following format::

	{ "sites":
	    [
       	      "http://masterchain.info/mastercoin_verify/addresses/0",
	      "https://masterchest.info/mastercoin_verify/addresses.aspx",
              "http://mymastercoins.com/jaddress.aspx"
	    ]
	}

Output:
^^^^^^^
Will return a json formated output array of address not in consensus

For each address not in Consensus, completed run will return balance of that address for each site checked in json format::

 {
   "consensus": Number Representing Consensus Rating,
   "data":[
      [
         {
            "balance": Number Representing Current balance for the site checked,
            "site":"Site/Data Source name",
            "address":"address not in consensus"
         },
	 {
	   ... data in format of ^ for each site when address is not in consensus
	 }
      ],
      [
         ... 2nd address (if exists) not in consensus in format ^^^
      ]
   ]
 }


Running:
^^^^^^^^
Running by creating a json file (see input details) for sites you wish to check or use the provided getConsensus.json
You can execute/run the program with::

 cat getConsensus.json | python getConsensusMSC.py

