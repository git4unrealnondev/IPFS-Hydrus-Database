import ipfshttpclient

import requests
import urllib3

import os
import json

def makeConnection():
	return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
	
#if __name__ == '__main__':
#	makeConnection()
#	dison = {}
#	dison["A"] = "B"
#	dison["C"] = "D"
#	lkj = json.dumps(dison)
#	file = open("json.txt", "w")
#	file.write(json.dumps(dison))
#	file.close()
#	print (lkj)



class hydrusSetup():
	access_key = None
	ip = "127.0.0.1"
	port = 45869
	conf = "conf.json"
	
	def __init__(self):

		if (os.path.exists(self.conf)):
			with open(self.conf, 'r') as myfile:
				data=myfile.read()
				obj = json.loads(data)
				self.access_key = str(obj['access_key'])
				self.ip = str(obj['ip'])
				self.port = str(obj['port'])
				myfile.close()
		else:
			self.initialConnect()
			dison = {}
			dison["access_key"] = self.access_key
			dison["ip"] = self.ip
			dison["port"] = self.port
			with open(self.conf, 'w') as myfile:
				myfile.write(json.dumps(dison))
				myfile.close()
				
	def initialConnect(self):
		ReqHeader = {'User-Agent': 'Hydrus Utilize - Mobile'}
		try:
			r = requests.get('http://' + str(self.ip) + ':45869' + '/request_new_permissions?' + 
				'name=Hydrus%20IPFS%20Searcher&basic_permissions=[0,1,2,3,4]', 
				headers=ReqHeader)
		except:
			print ("Error Connecting to client: is it currently accepting API Requests?")
			print ("Go to Services -> Manage Services -> Client API and uncheck do not run client service.")
			quit()
		if (r.status_code == 409):
			print ("Client is on and not accepting API requests go to:")
			print ("Services -> Review Services -> Client API -> add -> from api request")
			quit()
		else:
			self.access_key = json.loads(r.content)["access_key"]
			return
## Share TCP connections using a context manager
#with ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') as client:
#	hash = client.add('test.txt')['Hash']
#	key =client.object.put("HYDRUSDB-FILE")
#	print(key)
#	print(key["Hash"])
	
main = hydrusSetup()

