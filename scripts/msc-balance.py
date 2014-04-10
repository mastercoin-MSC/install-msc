#get balance
import sys
import json
import operator, os.path
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

#Read User Input
JSON = sys.stdin.readlines()
listOptions = json.loads(str(''.join(JSON)))

addr = listOptions['address']
currency = listOptions['currency_id']

#Check if revision file exist
if not os.path.isfile(DATA+REV):
    print json.dumps({ "address": addr, "currency": currency, "balance": "Error, No revision data. Is data parsed/validated."})
    exit()



#check the age of our data, 30+min is to old
#now = time.strftime("%s")
#checkTime = int(now) - 1800
revFile = open(DATA+REV, 'r')
revOptions = json.loads(revFile.read())
revFile.close()
parsedTime = calendar.timegm( time.strptime(revOptions['last_parsed'], '%d %b %Y %H:%M:%S %Z'))


#if parsedTime < checkTime and not force:
#    print json.dumps({ "address": addr, "currency": currency, "balance": "Error, Balance Data older than 30min"})
#    exit()



#parse the verified balances of currency for address
if currency == 1:
    #msc
    try:
       json_file = open(DATA+CID+'0', 'r')
    except IOError:
       print json.dumps({ "address": addr, "currency": currency, "balance": "Error, Can't Open Address file"+DATA+CID+"0"})
       exit()      
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
    try:
       json_file = open(DATA+CID+'1', 'r')
    except IOError:
       print json.dumps({ "address": addr, "currency": currency, "balance": "Error, Can't Open Address file"+DATA+CID+"1"})
       exit()
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
print json.dumps({ "address": addr, "currency": currency, "balance": balance, "balancetime": revOptions['last_parsed'], "balanceepoch": parsedTime})
