#get balance
import sys
import json
import requests
import urlparse

if len(sys.argv) > 1: 
    print "Takes a list of MSC consensus sites and outputs a consensus rating with the non-matching balances\nUsage: cat getConsensus.json | python getConsensusMSC.py\n"
    exit()

JSON = sys.stdin.readlines()

listSites = json.loads(str(''.join(JSON)))
results = []
for site in listSites['sites']:
	#print str(urlparse.urlsplit(site).netloc)
	res = requests.get(site)
	data = res.json()
	#f=open('./'+
	results.append({"data": data, "length": len(data), "site": str(urlparse.urlsplit(site).netloc) })

#Local data parsed by sx
DATA='/var/lib/mastercoin-tools/www/mastercoin_verify/addresses/'

json_file = open(DATA+'0', 'r')
ldata = json.loads(json_file.read())
json_file.close()
results.append({"data": ldata, "length": len(ldata), "site": "Local" })

	
longest = { "length": 0, "site": None }
for site in results:
	if site['length'] >= longest['length']:
		longest = { "length": site['length'], "site": site['site'] }

addresses = []
for site in results:
	if site['site'] == longest['site']:
		for summary in site['data']:
			addresses.append(summary['address'])
finalcount = []
for address in addresses:
	#print type(str(address))
	#print address
	addrstruct = []
	for site in results:
		for summary in site['data']:
			if str(summary['address']) == str(address):
				addrstruct.append({ "address": summary['address'], "balance": float(summary['balance']), "site": site['site'] })
	if not all(struct['balance'] == addrstruct[0]['balance'] for struct in addrstruct):
		#print addrstruct
		if addrstruct != []:
			finalcount.append(addrstruct)

consensus = 100*(1-float(len(finalcount))/float(longest['length']))
print json.dumps({ "consensus": consensus, "data": finalcount})
#balance and address
