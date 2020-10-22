import ipfshttpclient

import json

def makeConnection():
	return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
	
if __name__ == '__main__':
	makeConnection()
	dison = {}
	dison["A"] = "B"
	dison["C"] = "D"
	lkj = json.dumps(dison)
	file = open("json.txt", "w")
	file.write(json.dumps(dison))
	file.close()
	print (lkj)
# Share TCP connections using a context manager
with ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') as client:
	hash = client.add('test.txt')['Hash']
	key =client.object.put("HYDRUSDB-FILE")
	print(key)
	print(key["Hash"])
	
