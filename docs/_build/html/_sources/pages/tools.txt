=====
Tools
=====

List of tools included with the isntallation and how to use them

msc_sxsend.py
-------------

Purpose:
^^^^^^^^
Used to create (and/or send) a Mastercoin transaction

Inputs:
^^^^^^^
Takes json input via STDIN for the following variables:

* transaction_from: The Public Address of the Sender
* transaction_from_pubkey_comp: If the sending address has not been used before you can provide the Compressed Public Key here
* transaction_to: The Public address of the Receipiant
* currency_id: Currency ID to send. 1 for MSC, 2 for TMSC
* msc_send_amt: The amount of the Currency ID to send
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
	  "transaction_from_pubkey_comp": "{{Compressed Public Key if address has not sent to blockchain yet}}",
	  "transaction_to": "{{Public to Address}}",
	  "currency_id": {{1 for MSC, 2 for TMSC}},
	  "msc_send_amt": {{amount to send}},
	  "from_private_key": "{{private key for signing}}",
	  "broadcast": {{1 to create and broadcast or 0 to just create}},
          "clean": {{0 -keep all tx files, 1 -remove intersigned tx, 2 -remove all unsigned, 3 -remove all}}
	}

Ex:

*Note: for security the following was a brand new empty wallet. You should replace it's details with your own applicable info*::

	{
	  "transaction_from": "1CMauYumpA7YG8i4cPod8FadRLK95HxSob",
	  "transaction_from_pubkey_comp": "0368d7c560e7376596dfa574b28badde241a80309f4fbbba204c2034e5ed4fa353",
	  "transaction_to": "19hf8QEkD3GR7NhUrujWXRg6e4gsHUTysp",
	  "currency_id": 1,
	  "msc_send_amt": 5.1,
	  "from_private_key": "KzPeWRBj1qDfLZNsDyFrWdnfi4cdoqxHWkkJ2pedRVKtEMEh2oxE",
	  "broadcast": 1
          "clean": 1
	}

For reference, here is what the brainwallet.org generator page for the above address looks like.
Take note of the 'Compressed' option 

.. image:: brainwallet.png
    :align: center

Output:
^^^^^^^
Will return a json formated output
Errors will be returned with json that contains ::

 { 
    "status": "Status message", 
    "error": "error details", 
    "fix": "Corrective action to resolve the issue"
 }

Successful run will return json that contains::

 { "status": "Broadcast/Created status", 
   "valid_check": "Validity check of signed file", 
   "hash": "Hash of the tx", 
   "st_file": "location/name of the signed tx file"
 }

Running:
^^^^^^^^
Standalone running/testing can be done by creating a json file (see input details or example_send.json for structure)
You can execute/run the program with::

 cat your_file.json | python msc_sxsend.py
