#get balance
import sys
import json
import operator
import time,  calendar

if len(sys.argv) > 1 and "--force" not in sys.argv: 
    print "Takes addresses and currency in JSON and outputs balance in JSON \nUsage: cat address.json | python msc-balance.py\nRequires mastercoin-tools updated and synced"
    exit()

if "--force" in sys.argv:
    #WARNING: '--force' WILL STEAL YOUR BITCOINS IF YOU DONT KNOW WHAT YOU'RE DOING
    force=True
else:
    force=False



#where is the data stored (mastercoin-tools outputs to here)
DATA="/var/lib/mastercoin-tools/"
CID="mastercoin_verify/addresses/"
REV="www/revision.json"

#check the age of our data, 30+min is to old
now = time.strftime("%s")
checkTime = int(now) - 1800
revFile = open(DATA+REV, 'r')
revOptions = json.loads(revFile.read())
revFile.close()
parsedTime = calendar.timegm( time.strptime(revOptions['last_parsed'], '%d %b %Y %H:%M:%S %Z'))


JSON = sys.stdin.readlines()
listOptions = json.loads(str(''.join(JSON)))

addr = listOptions['address']
currency = listOptions['currency_id']

if parsedTime < checkTime and not force:
    print json.dumps({ "address": addr, "currency": currency, "balance": "Error, Balance Data older than 30min"})
    exit()



#parse the verified balances of currency for address
if currency == 1:
    #msc
    json_file = open(DATA+CID+'0', 'r')
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
    json_file = open(DATA+CID+'1', 'r')
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




#print os.path.getmtime(json_file.name)
#print time.getnow()

#return our final output
print json.dumps({ "address": addr, "currency": currency, "balance": balance})
