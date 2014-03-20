#get balance
import sys
import json
import operator

if len(sys.argv) > 1: 
    print "Takes addresses and currency in JSON and outputs balance in JSON \nUsage: cat address.json | python msc-balance.py\nRequires mastercoin-tools updated and synced"
    exit()

#where is the data stored (mastercoin-tools outputs to here)
DATA="/var/lib/mastercoin-tools/mastercoin_verify/addresses/"
#DATA="./"

JSON = sys.stdin.readlines()
listOptions = json.loads(str(''.join(JSON)))

addr = listOptions['address']
currency = listOptions['currency_id']

#parse the verified balances of currency for address
if currency == 1:
    #msc
    json_file = open(DATA+'0', 'r')
    al = json.loads(json_file.read())
    json_file.close()
    for output in al:
	if output['address'] == addr:
		balance = output['balance']
		break
	else:
	        balance = 'Error - Address Not Found'
elif currency == 2:
    #tmsc
    json_file = open(DATA+'1', 'r')
    al = json.loads(json_file.read())
    json_file.close()
    for output in al:
        if output['address'] == addr:
                balance = output['balance']
                break
        else:
                balance = 'Error - Address Not Found'
else:
    balance = 'Error - Invalid Currency'

#return our final output
print json.dumps({ "address": addr, "currency": currency, "balance": balance})
