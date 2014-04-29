#!/usr/bin/python
#Send Masterprotocol Currencies using db tracking of utxo
import sys
import json
import time
import random
import hashlib
import operator
import commands
import pybitcointools
import os, decimal
import requests, urlparse
from pycoin import encoding
from msc_utils_send import *

if len(sys.argv) > 1 and "--force" not in sys.argv: 
    print "Takes a list of bitcoind options, addresses and a send amount and outputs a transaction in JSON \nUsage: cat send.json | python msc-sxsend.py\nRequires sx and a configured obelisk server"
    exit()

if "--force" in sys.argv:
    #WARNING: '--force' WILL STEAL YOUR BITCOINS IF YOU DON KNOW WHAT YOU'RE DOING
    force=True
else:
    force=False

JSON = sys.stdin.readlines()
try:
    listOptions = json.loads(str(''.join(JSON)))
except ValueError:
    print json.dumps({ "status": "NOT OK", "error": "Couldn't read input variables", "fix": "check input data"+str(JSON) })
    exit()

#get local running dir
RDIR=os.path.dirname(os.path.realpath(__file__))

#Define and make sure we have a data dir
DATA=RDIR+'/data/'
commands.getoutput('mkdir -p '+DATA)

#get some variables from the json iput
FROMADDRESS=listOptions['transaction_from']
TOADDRESS=listOptions['transaction_to']
CID=listOptions['currency_id']
TOAMOUNT=listOptions['send_amt']
PTYPE=listOptions['property_type']
BROADCAST=listOptions['broadcast']
CLEAN=1
if BROADCAST == 1:
    PRIVATE_KEY=listOptions['from_private_key']
    CLEAN=listOptions['clean']
    #check if private key provided produces correct address
    address = pybitcointools.privkey_to_address(PRIVATE_KEY)
    if not address == FROMADDRESS and not force:
    	print json.dumps({ "status": "NOT OK", "error": "Private key does not produce same address as \'transaction from\'" , "fix": "Set \'force\' flag to proceed without address checks" })
    	exit()

#prime out utxo files
if sync_utxo(FROMADDRESS) == 1:
    print json.dumps({ "status": "NOT OK", "error": "Couldn't update utxo list", "fix": "Check connection to internet, sx operating properly and try again" })
    exit()

#calculate minimum unspent balance (everything in satoshi's)
available_balance = int(0)
utxo_array=get_utxo()
for item in utxo_array:
    if item['address'] == FROMADDRESS:
        available_balance += int(item['satoshi'])

#BAL = commands.getoutput('sx balance -j '+listOptions['transaction_from'])
#balOptions = json.loads(str(''.join(BAL)))
#available_balance = int(balOptions[0]['paid'])

broadcast_fee = int(10000)
output_minimum = int(5500) #dust threshold 5460

fee_total = broadcast_fee + (output_minimum * 4)

#check if minimum BTC balance is met
if available_balance < fee_total and not force:
    print json.dumps({ "status": "NOT OK", "error": "Not enough funds "+str(available_balance)+" of "+str(fee_total), "fix": "Make sure db tx are updated and you have enough btc" })
    exit()

#check if Currency ID balance is available
#print json.dumps({ "address": addr, "currency": currency, "balance": balance})
#cid_query = '{ \\"address\\": \\"'+listOptions['transaction_from']+'\\", \\"currency_id\\": '+str(listOptions['currency_id'])+'}'

#if force:
#    cid_balance = json.loads(commands.getoutput('echo '+cid_query+' | python '+RDIR+'/msc-balance.py --force '))['balance']
#else:
#    cid_balance = json.loads(commands.getoutput('echo '+cid_query+' | python '+RDIR+'/msc-balance.py'))['balance']

#get balance from omniwallet web interface
if CID == 1:
    cid_balance=get_balance(FROMADDRESS, 'MSC',2)
elif CID == 2:
    cid_balance=get_balance(FROMADDRESS, 'TMSC',2)
else:
    cid_balance=get_balance(FROMADDRESS, 'SP'+str(CID),PTYPE)

try:
    float(cid_balance)
except ValueError:
    print json.dumps({"status": "NOT OK", "error": cid_balance , "fix": "Make sure Balance data is up to date: "})
    exit()

if  float(cid_balance) < float(TOAMOUNT) and not force:
    print json.dumps({"status": "NOT OK", "error": "Currency ID balance too low" , "fix": "Check Currency ID balance: "+str(cid_balance)})
    exit()

#generate public key of bitcoin address from priv key
#validated = commands.getoutput('sx get-pubkey '+listOptions['transaction_from'])

#get pubkey from blockchain
PUBLIC_KEY = commands.getoutput('sx get-pubkey '+FROMADDRESS)
#pubkey = commands.getoutput('echo '+listOptions['from_private_key']+' | sx pubkey')
if is_pubkey_valid(PUBLIC_KEY):
    pass
else:
    #check if we are broadcasting and try to generate pubkey
    if BROADCAST == 1:
	PUBLIC_KEY = commands.getoutput('echo '+PRIVATE_KEY+' | sx pubkey')
	if is_pubkey_valid(PUBLIC_KEY):
	    pass
	else:
	    print json.dumps({ "status": "NOT OK", "error": "from address is invalid or hasn't been used on the network" , "fix": "Check from address or provide from address public key. Alternatively Set \'force\' flag to proceed without balance checks" })
	    exit()
    else:
	print json.dumps({ "status": "NOT OK", "error": "from address is invalid or hasn't been used on the network" , "fix": "Check from address or provide from address public key. Alternatively Set \'force\' flag to proceed without balance checks" })
	exit()

#get unspent tx to use for creating our input
tx_unspent_bal=0
utxo_list=[]
for item in utxo_array:
    if item['address'] == FROMADDRESS and item['lock'] == '1':
        tx_unspent_bal += int(item['satoshi'])
	utxo_list.append(item)
	item['lock'] = 2
	if tx_unspent_bal >= fee_total:
	    break

#real stuff happens here:

# calculate change : 
# (total input amount) - (broadcast fee) - (total transaction fee)

change = int(tx_unspent_bal) - fee_total
if change < 0 or fee_total > available_balance and not force:
    print json.dumps({ "status": "NOT OK", "error": "Not enough funds "+str(available_balance)+" of "+str(fee_total), "fix": "Send some btc to the sending address. Check db tx to make sure they are accurate" })
    exit()

#build multisig data address
transaction_type = 0   #simple send
sequence_number = 1    #packet number
#currency_id = 2        #MSC=1, TMSC=2
currency_id = int(CID)
#amount = int(float(listOptions['msc_send_amt'])*1e8)  #maran's impl used float??
amount = int(decimal.Decimal(TOAMOUNT)*decimal.Decimal("1e8"))

cleartext_packet = ( 
        (hex(sequence_number)[2:].rjust(2,"0") + 
            hex(transaction_type)[2:].rjust(8,"0") +
            hex(currency_id)[2:].rjust(8,"0") +
            hex(amount)[2:].rjust(16,"0") ).ljust(62,"0") )

sha_the_sender = hashlib.sha256(FROMADDRESS).hexdigest().upper()[0:-2]
# [0:-2] because we remove last ECDSA byte from SHA digest

cleartext_bytes = map(ord,cleartext_packet.decode('hex'))  #convert to bytes for xor
shathesender_bytes = map(ord,sha_the_sender.decode('hex')) #convert to bytes for xor

msc_data_key = ''.join(map(lambda xor_target: hex(operator.xor(xor_target[0],xor_target[1]))[2:].rjust(2,"0"),zip(cleartext_bytes,shathesender_bytes))).upper()
#map operation that xor's the bytes from cleartext and shathesender together
#to obfuscate the cleartext packet, for more see Appendix Class B:
#https://github.com/faizkhan00/spec#class-b-transactions-also-known-as-the-multisig-method

obfuscated = "02" + msc_data_key + "00" 
#add key identifier and ecdsa byte to new mastercoin data key

invalid = True
while invalid:
    obfuscated_randbyte = obfuscated[:-2] + hex(random.randint(0,255))[2:].rjust(2,"0").upper()
    #set the last byte to something random in case we generated an invalid pubkey
    potential_data_address = pybitcointools.pubkey_to_address(obfuscated_randbyte)
    if bool(commands.getoutput('sx validaddr '+potential_data_address)):
        data_pubkey = obfuscated_randbyte
        invalid = False
#make sure the public key is valid using pybitcointools, if not, regenerate 
#the last byte of the key and try again

#### Build transaction
#retrieve raw transaction data to spend it and add it to the input 
validnextinputs=""
input_counter=0
for utxo in utxo_list:
  #prev_tx = json.loads(commands.getoutput('sx fetch-transaction '+utxo[0]+' | sx showtx -j'))
   try:
        prev_tx = json.loads(commands.getoutput('sx fetch-transaction '+utxo['tx_hash']+' | sx showtx -j'))
   except ValueError:
        print json.dumps({ "status": "NOT OK", "error": "Problem getting json format of utxo", "fix": "check utxo tx: "+str(utxo['tx_hash']) })
        exit()

   for output in prev_tx['outputs']:
      if output['address'] == FROMADDRESS:
          #validnextinputs+=str(" -i "+utxo[0]+":"+utxo[1])
          validnextinputs+=str(" -i "+str(utxo['tx_hash'])+":"+str(utxo['hash_index']))
	  input_counter+=1

#validnextoutputs add the exodus address and the receipiant to the output
#If change is less than dust but greater than 0 send it to the receipiant: Bonus!
to_fee=output_minimum
if change < output_minimum and change > 0:
    to_fee+=change

validnextoutputs="-o 1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P:"+str(output_minimum)+" -o "+TOADDRESS+":"+str(to_fee)

#if there's any leftover change above dust send it back to yourself
if change >= output_minimum: 
    validnextoutputs+=" -o "+FROMADDRESS+":"+str(change)

#create a temp file for the unsigned raw tx and the signed tx data for sx
#format: sender_address.recpt_address.secs_since_1970.random_hex
unsigned_raw_tx_file = DATA+FROMADDRESS+'.'+TOADDRESS+'.'+commands.getoutput('date +%s')+'.'+hex(random.randint(0,255))[2:].rjust(2,"0")
signed_raw_tx_file = unsigned_raw_tx_file+'.signed'

#store the unsigned tx data in the file
commands.getoutput('sx mktx '+unsigned_raw_tx_file+' '+validnextinputs+' '+validnextoutputs)

#convert it to json for adding the msc multisig
try:
    json_tx = json.loads(commands.getoutput('cat '+unsigned_raw_tx_file+' | sx showtx -j'))
except ValueError:
    print json.dumps({ "status": "NOT OK", "error": "Problem getting json format of unsigned_raw_tx", "fix": "check filename: "+str(unsigned_raw_tx_file) })
    exit()

#add multisig output to json object
json_tx['outputs'].append({ "value": output_minimum*2, "script": "1 [ " + PUBLIC_KEY + " ] [ " + data_pubkey.lower() + " ] 2 checkmultisig", "addresses": "null"})

#construct byte arrays for transaction 
#assert to verify byte lengths are OK
version = ['01', '00', '00', '00' ]
assert len(version) == 4

num_inputs = [str(len(json_tx['inputs'])).rjust(2,"0")]
assert len(num_inputs) == 1

num_outputs = [str(len(json_tx['outputs'])).rjust(2,"0")]
assert len(num_outputs) == 1

sequence = ['FF', 'FF', 'FF', 'FF']
assert len(sequence) == 4

blocklocktime = ['00', '00', '00', '00']
assert len(blocklocktime) == 4

#prepare inputs data for byte packing
inputsdata = []
for _input in json_tx['inputs']:
    prior_out_str = _input['previous_output'].split(':')
    #prior_input_txhash = _input['previous_output'].upper()  
    prior_input_txhash = prior_out_str[0].upper()  
    #prior_input_index = str(prior_out_str[1]).rjust(2,"0").ljust(8,"0")
    prior_input_index = str(hex(int(prior_out_str[1]))[2: ]).rjust(2,"0").ljust(8,"0")
    input_raw_signature = commands.getoutput('sx fetch-transaction '+prior_out_str[0])

    prior_txhash_bytes =  [prior_input_txhash[ start: start + 2 ] for start in range(0, len(prior_input_txhash), 2)][::-1]
    assert len(prior_txhash_bytes) == 32

    prior_txindex_bytes = [prior_input_index[ start: start + 2 ] for start in range(0, len(prior_input_index), 2)]
    assert len(prior_txindex_bytes) == 4

    len_scriptsig = ['%02x' % len(''.join([]).decode('hex').lower())] 
    assert len(len_scriptsig) == 1
    
    inputsdata.append([prior_txhash_bytes, prior_txindex_bytes, len_scriptsig])

#prepare outputs for byte packing
output_hex = []
for output in json_tx['outputs']:
    value_hex = hex(int(float(output['value'])))[2:]
    value_hex = value_hex.rjust(16,"0")
    value_bytes =  [value_hex[ start: start + 2 ].upper() for start in range(0, len(value_hex), 2)][::-1]
    assert len(value_bytes) == 8

    scriptpubkey_hex = commands.getoutput('sx rawscript '+output['script'])
    scriptpubkey_bytes = [scriptpubkey_hex[start:start + 2].upper() for start in range(0, len(scriptpubkey_hex), 2)]
    len_scriptpubkey = ['%02x' % len(''.join(scriptpubkey_bytes).decode('hex').lower())]

    output_hex.append([value_bytes, len_scriptpubkey, scriptpubkey_bytes] )

#join parts into final byte array
hex_transaction = version + num_inputs

for _input in inputsdata:
    hex_transaction += (_input[0] + _input[1] + _input[2] + sequence)

hex_transaction += num_outputs

for output in output_hex:
    hex_transaction = hex_transaction + (output[0] + output[1] + output[2]) 

hex_transaction = hex_transaction + blocklocktime

#prepare and populate unsigned_raw_tx_file
phash = ''.join(hex_transaction).lower()
commands.getoutput('echo '+phash+' > '+unsigned_raw_tx_file)

#verify that transaction is valid
pht = commands.getoutput('echo '+phash+' | sx showtx -j')

try:
   fc = json.loads(pht)
except ValueError, e:
    # invalid json
    print json.dumps({ "status": "NOT OK", "error": "unsigned tx not valid/malformed: "+pht, "fix": "Check your inputs/json file"})
    exit()
else:
    pass # valid json

if BROADCAST > 0:
#We will now sign the first input using our private key.
    DECODED_ADDR=commands.getoutput('echo '+PRIVATE_KEY+' | sx addr | sx decode-addr')
    PREVOUT_SCRIPT=commands.getoutput('sx rawscript dup hash160 [ '+DECODED_ADDR+' ] equalverify checksig')

    #Loop through and sign all the tx's inputs so we can create the final signed tx
    x=0
    commands.getoutput('cp '+unsigned_raw_tx_file+' '+unsigned_raw_tx_file+'.0')
    while x < input_counter:
        y=x+1
        SIGNATURE=commands.getoutput('echo '+PRIVATE_KEY+' | sx sign-input '+unsigned_raw_tx_file+' '+str(x)+' '+PREVOUT_SCRIPT)
        SIGNATURE_AND_PUBKEY_SCRIPT=commands.getoutput('sx rawscript [ '+SIGNATURE+' ] [ '+PUBLIC_KEY+' ]')
        commands.getoutput('sx set-input '+unsigned_raw_tx_file+'.'+str(x)+' '+str(x)+' '+SIGNATURE_AND_PUBKEY_SCRIPT+' > '+unsigned_raw_tx_file+'.'+str(y))  # the first input has index 0
        x+=1

    commands.getoutput('cp '+unsigned_raw_tx_file+'.'+str(y)+' '+signed_raw_tx_file)

    #loop through external command 3 times in case it times out
    z=0
    while z < 3:
	tx_valid=commands.getoutput('sx validtx '+signed_raw_tx_file)
	if "Success" in tx_valid:
	    z=4
	else:
	    z+=1

    if "Success" not in tx_valid:
        print json.dumps({ "status": "NOT OK", "error": "signed tx not valid/failed sx validation: "+tx_valid, "fix": "Check inputs/json file"})
        exit()

    try:
        tx_hash=json.loads(commands.getoutput('cat '+signed_raw_tx_file+' | sx showtx -j'))['hash']
    except ValueError:
        print json.dumps({ "status": "NOT OK", "error": "Problem getting json format of signed_raw_tx_file", "fix": "check filename: "+str(signed_raw_tx_file) })
        exit()

    #broadcast to obelisk node if requested
    if BROADCAST == 2:
	bcast_status=commands.getoutput('sx sendtx-obelisk '+signed_raw_tx_file)
    else:
	bcast_status="out: Created/Signed, Not Sent"
else:
    bcast_status="out: Created, Not Signed/Not Sent"
    tx_valid="TX Unsigned, not checked"
    try:
        tx_hash=json.loads(commands.getoutput('cat '+unsigned_raw_tx_file+' | sx showtx -j'))['hash']
    except ValueError:
        print json.dumps({ "status": "NOT OK", "error": "Problem getting json format of unsigned_raw_tx_file", "fix": "check filename: "+str(unsigned_raw_tx_file) })
        exit()


#update out utxo files
write_utxo(utxo_array)

if CLEAN == 0:
    #clean nothing
    pass
elif CLEAN == 1:
    #remove intermediary unsigned files
    x=0
    while x <= input_counter:
        commands.getoutput('rm '+unsigned_raw_tx_file+'.'+str(x))
        x+=1
elif CLEAN == 2:
    #remove all unsigned files
    x=0
    commands.getoutput('rm '+unsigned_raw_tx_file)
    while x <= input_counter:
        commands.getoutput('rm '+unsigned_raw_tx_file+'.'+str(x))
        x+=1
elif CLEAN == 3:
    #remove signed and unsigned files (everything)
    commands.getoutput('rm '+unsigned_raw_tx_file)
    commands.getoutput('rm '+unsigned_raw_tx_file+'.*')
    signed_raw_tx_file='Cleaned/removed by request'

#return our final output
if BROADCAST > 0:
    print json.dumps({ "status": bcast_status.split(':')[1], "valid_check": tx_valid.split(':')[1], "hash": tx_hash, "st_file": signed_raw_tx_file})
else:
    print json.dumps({ "status": bcast_status.split(':')[1], "valid_check": tx_valid, "hash": tx_hash, "st_file": unsigned_raw_tx_file})
