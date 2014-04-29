#!/usr/bin/python
#Function Definitions for send utils
import sys
import json
import time
import random
import hashlib
import operator
import commands, csv
import pybitcointools
import os, decimal
import requests, urlparse
from pycoin import encoding
from ecdsa import curves, ecdsa

def is_pubkey_valid(pubkey):
    try:
        sec=encoding.binascii.unhexlify(pubkey)
        public_pair=encoding.sec_to_public_pair(sec)
        return curves.ecdsa.point_is_valid(ecdsa.generator_secp256k1, public_pair[0], public_pair[1])
    except TypeError:
        return False

#get all the utxo we are tracking
def get_utxo():
    list=[]
    try:
	with open('utxolist.csv') as f:
	    reader = csv.DictReader(f, delimiter=',')
	    for row in reader:
	        list.append(row)
    except IOError:
	commands.getoutput('touch utxolist.csv')
    return list

def write_utxo(listdata):
    with open('utxolist.csv', "wb") as out_file:
	writer = csv.DictWriter(out_file, delimiter=',', fieldnames=["address","tx_hash","hash_index","satoshi","block","lock"])
	writer.writeheader()
	for row in listdata:
	    writer.writerow(row)

#def get_utxo_db(address):
#    con=None
#    ROWS=[]
#    try:
#        con = psycopg2.connect(database=DBNAME, user=DBUSER)
#        dbc = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#        dbc.execute("select * from tx_utxo where lock='1' and address='%s' order by satoshi desc;" % str(address))
#        ROWS = dbc.fetchall()
#    except psycopg2.DatabaseError, e:
#        print json.dumps({"status": "DB Update Error", "error": e , "fix": "Check files/db status and try again "})
#        sys.exit(1)
#    finally:
#        if con:
#            con.close()
#        return ROWS

#def update_db(txlist, status):
#    con=None
#    try:
#        con = psycopg2.connect(database=DBNAME, user=DBUSER)
#        dbc = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#        if "Success" in status.split(':')[1]:
#          for x in txlist:
#            dbc.execute("update tx_utxo set lock='2' where id=%s;" % int(x['id']))
#            con.commit()
#        else:
#          for x in txlist:
#            dbc.execute("update tx_utxo set lock='3' where id=%s;" % x['id'])
#            con.commit()
#    except psycopg2.DatabaseError, e:
#        print json.dumps({"status": "DB Update Error", "error": e , "fix": "Check files/db status and try again "})
#        sys.exit(1)
#    finally:
#        if con:
#            con.close()

def get_balance(address, csym, div):
    bal1=-3
    bal2=-4
    url =  'https://test.omniwallet.org/v1/address/addr/'
    PAYLOAD = {'addr': address }
    try:
        tx_data= requests.post(url, data=PAYLOAD, verify=False).json()
        for bal in tx_data['balance']:
            if csym == bal['symbol']:
                if div == 1:
                    bal1=('%.8f' % float(bal['value']))
                else:
                    fbal=float(bal['value'])/100000000
                    bal1=('%.8f' % fbal)
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        #print('Site 1 Unresponsive, Using 0 balance for now')
        bal1=-1

    url2 = 'https://www.masterchest.info/mastercoin_verify/adamtest.aspx?address='+address
    try:
        tx2_data=requests.get(url2, verify=False).json()
        for bal in tx2_data['balance']:
            if csym == bal['symbol']:
                bal2= ('%.8f' % float(bal['value']))
    except ValueError:  # includes simplejson.decoder.JSONDecodeError
        #print('Site 2 Unresponsive, Using 0 balance for now')
        bal2=-2

    if bal1 == bal2:
        #print(' Confirmed Balance of '+str(bal1)+' '+str(csym)+' for '+str(address)+' from 2 data points')
        return bal1
    elif bal1 > 0 and bal2 < 0:
        #print(' Balance mismatch, Site 1:['+str(bal1)+'] Site 2:['+str(bal2)+'] '+str(csym)+' for '+str(address)+' $
        return bal1
    else:
        #print(' Balance mismatch, Site 1:['+str(bal1)+'] Site 2:['+str(bal2)+'] '+str(csym)+' for '+str(address)+' $
        return bal2


def sync_utxo(address):
	z=0
	while z < 3:
	    current_block = commands.getoutput('/usr/local/bin/sx fetch-last-height')
	    try: 
		int(current_block)
		z=4
	    except ValueError:
		pass
	    z+=1

	try:
            int(current_block)
        except ValueError:
            return 1

	utxo_list=[] 
	utxo_list=get_utxo()
	updated_list=[]
	for item in utxo_list:
	    if item['lock'] == '2' and int(item['block']) > int(current_block)-10:
		updated_list.append(item)
        lsi_array=[]
        sx_mon = commands.getoutput('sx balance '+address).replace(" ", "").splitlines()
        #Catch unknown sx output and skip this time
        if len(sx_mon)==4:
          address_satoshi_max=int(sx_mon[1].split(":")[1])
          #find largest spendable input from UTXO
          #todo, add ability to use multiple smaller tx to do multi input funding
          nws = (commands.getoutput('sx get-utxo '+address+" "+str(address_satoshi_max))).replace(" ", "")
          #since sx doesn't provide a clean output we need to try and clean it up and get the usable outputs
          for x in nws.splitlines():
               lsi_array.append(x.split(':'))
        if len(lsi_array) > 5:
            #data_utxo=[]
            for i in range(0, len(lsi_array),8):
                address=lsi_array[i][1]
                tx_hash=lsi_array[i+1][1]
                tx_hash_index=lsi_array[i+1][2]
                block_height=lsi_array[i+2][1]
                satoshi=lsi_array[i+3][1]
		#print(address+" "+tx_hash+" "+tx_hash_index+" "+block_height+" "+satoshi)
		if len(updated_list) == 0:
		    updated_list.append({'address':address,'tx_hash':tx_hash,'hash_index':tx_hash_index,'satoshi':satoshi,'block':current_block,'lock':1})
		else:
		    u=1
	            for item in updated_list:
	            	if item['address'] == address and item['tx_hash'] == tx_hash and item['hash_index'] == tx_hash_index:
			    u=0
			    break
		    if u == 1:
			    updated_list.append({'address':address,'tx_hash':tx_hash,'hash_index':tx_hash_index,'satoshi':satoshi,'block':current_block,'lock':1})
	    write_utxo(updated_list)
        else:
	    pass
            #print ('No new transactions to update')
	return 0
