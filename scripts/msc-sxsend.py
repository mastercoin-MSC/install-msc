#get balance
import sys
import json
import time
import random
import hashlib
import operator
import commands
import pybitcointools
from decimal import *
from pycoin import encoding
from ecdsa import curves, ecdsa

def is_pubkey_valid(pubkey):
    try:
        sec=encoding.binascii.unhexlify(pubkey)
        public_pair=encoding.sec_to_public_pair(sec)
        return curves.ecdsa.point_is_valid(ecdsa.generator_secp256k1, public_pair[0], public_pair[1])
    except TypeError:
        return False


if len(sys.argv) > 1 and "--force" not in sys.argv: 
    print "Takes a list of bitcoind options, addresses and a send amount and outputs a transaction in JSON \nUsage: cat generateTx.json | python generateTx.py\nRequires a fully-synced *local* bitcoind node"
    exit()

if "--force" in sys.argv:
    #WARNING: '--force' WILL STEAL YOUR BITCOINS IF YOU DON KNOW WHAT YOU'RE DOING
    force=True
else:
    force=False

JSON = sys.stdin.readlines()

listOptions = json.loads(str(''.join(JSON)))

#check if private key provided produces correct address
address = pybitcointools.privkey_to_address(listOptions['from_private_key'])
if not address == listOptions['transaction_from'] and not force:
    print json.dumps({ "status": "NOT OK", "error": "Private key does not produce same address as \'transaction from\'" , "fix": "Set \'force\' flag to proceed without address checks" })
    exit()

    private = listOptions['from_private_key']

#calculate minimum unspent balance (everything in satoshi's)
available_balance = int(0)

BAL = commands.getoutput('sx balance -j '+listOptions['transaction_from'])
balOptions = json.loads(str(''.join(BAL)))
available_balance = int(balOptions[0]['paid'])

broadcast_fee = int(10000)
output_minimum = int(5555) #dust threshold

fee_total = broadcast_fee + (output_minimum * 4)
change = available_balance - fee_total


#check if minimum BTC balance is met
if available_balance < fee_total and not force:
    print json.dumps({ "status": "NOT OK", "error": "Not enough funds" , "fix": "Set \'force\' flag to proceed without balance checks" })
    exit()

#generate/get public key of bitcoin address 
validated = commands.getoutput('sx get-pubkey '+listOptions['transaction_from'])
if "ddress" not in validated:
    pubkey = validated
elif is_pubkey_valid(listOptions['transaction_from_pubkey_comp']):
    pubkey = listOptions['transaction_from_pubkey_comp']
elif not force:
    print json.dumps({ "status": "NOT OK", "error": "from address is invalid or hasn't been used on the network" , "fix": "Set \'force\' flag to proceed without balance checks" })
    exit()

#find largest spendable input from UTXO
#find a recent tx that has a balance more than msc send cost (4*.00005500 +.0001 = .00032220)
#todo, add ability to use multiple smaller tx to do multi input funding
nws = (commands.getoutput('sx get-utxo '+listOptions['transaction_from']+" "+str(fee_total))).replace(" ", "")

lsi_array=[]
#since sx doesn't provide a clean output we need to try and clean it up and get the usable outputs
for x in nws.splitlines():
  lsi_array.append(x.split(':'))

z=0
for item in lsi_array:
  if lsi_array[z][0] == "output":
	largest_spendable_input=(lsi_array[z][1],lsi_array[z][2])
  z += 1

#real stuff happens here:

# calculate change : 
# (total input amount) - (broadcast fee) - (total transaction fee)

if change < 0 or fee_total > available_balance and not force:
    print json.dumps({ "status": "NOT OK", "error": "Not enough funds" , "fix": "Set \'force\' flag to proceed without balance checks" })
    exit()

#build multisig data address

from_address = listOptions['transaction_from']
transaction_type = 0   #simple send
sequence_number = 1    #packet number
currency_id = 2        #TMSC
amount = int(listOptions['msc_send_amt']*1e8)  #maran's impl used float??

cleartext_packet = ( 
        (hex(sequence_number)[2:].rjust(2,"0") + 
            hex(transaction_type)[2:].rjust(8,"0") +
            hex(currency_id)[2:].rjust(8,"0") +
            hex(amount)[2:].rjust(16,"0") ).ljust(62,"0") )

sha_the_sender = hashlib.sha256(from_address).hexdigest().upper()[0:-2]
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

#retrieve raw transaction data to spend it
prev_tx = json.loads(commands.getoutput('sx fetch-transaction '+largest_spendable_input[0]+' | sx showtx -j'))

for output in prev_tx['outputs']:
   if output['address'] == listOptions['transaction_from']:
       validnextinputs="-i "+largest_spendable_input[0]+":"+largest_spendable_input[1]


#validnextoutputs add the exodus address and the receipiant to the output
validnextoutputs="-o 1EXoDusjGwvnjZUyKkxZ4UHEf77z6A5S4P:"+str(output_minimum)+" -o "+listOptions['transaction_to']+":"+str(output_minimum)

#if there's any leftover change above dust send it back to yourself
if change > Decimal(0.00006): 
    validnextoutputs+=" -o "+listOptions['transaction_from']+":"+str(change)

#create a temp file for the unsigned raw tx and the signed tx data for sx
unsigned_raw_tx_file = 'data/'+listOptions['transaction_from']+'.'+listOptions['transaction_to']+'.'+commands.getoutput('date +%s')
signed_raw_tx_file = unsigned_raw_tx_file+'.signed'

#store the unsigned tx data in the file
commands.getoutput('sx mktx '+unsigned_raw_tx_file+' '+validnextinputs+' '+validnextoutputs)

#convert it to json for adding the msc multisig
json_tx = json.loads(commands.getoutput('cat '+unsigned_raw_tx_file+' | sx showtx -j'))

#add multisig output to json object
json_tx['outputs'].append({ "value": output_minimum*2, "script": "1 [ " + pubkey + " ] [ " + data_pubkey.lower() + " ] 2 checkmultisig", "addresses": "null"})

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
    prior_input_index = str(prior_out_str[1]).rjust(2,"0").ljust(8,"0")
    input_raw_signature = commands.getoutput('sx fetch-transaction '+prior_out_str[0])

    #print prior_out_str    

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

#verify that transaction is valid
phash = ''.join(hex_transaction).lower()
commands.getoutput('echo '+phash+' > '+unsigned_raw_tx_file)
pht = commands.getoutput('echo '+phash+' | sx showtx -j')
#assert type(pht) == type({})


#We will now sign the first input using our private key.

PRIVATE_KEY = ''+listOptions['from_private_key']
PUBLIC_KEY=commands.getoutput('echo '+PRIVATE_KEY+' | sx pubkey')
DECODED_ADDR=commands.getoutput('echo '+PRIVATE_KEY+' | sx addr | sx decode-addr')
PREVOUT_SCRIPT=commands.getoutput('sx rawscript dup hash160 [ '+DECODED_ADDR+' ] equalverify checksig')
SIGNATURE=commands.getoutput('echo '+PRIVATE_KEY+' | sx sign-input '+unsigned_raw_tx_file+' 0 '+PREVOUT_SCRIPT)
SIGNATURE_AND_PUBKEY_SCRIPT=commands.getoutput('sx rawscript [ '+SIGNATURE+' ] [ '+PUBLIC_KEY+' ]')
commands.getoutput('sx set-input '+unsigned_raw_tx_file+' 0 SIGNATURE_AND_PUBKEY_SCRIPT > '+signed_raw_tx_file)  # the first input has index 0


print "signed file prepared: "+signed_raw_tx_file

#broadcast to obelisk node
#commands.getoutput('sx sendtx-obelisk '+signed_raw_tx_file)
