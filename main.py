import ipfshttpclient

import requests
import urllib

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

class IPFS():
	def __init__(self):
		print ("Connecting to IPFS")
		self.client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
		self.pinLS()
	def addPin(self, fileLocation):
		return self.client.add(fileLocation, pin = True)

	def pinLS(self):
		aList = self.client.pin.ls()

		json_Obj = aList["Keys"]
		self.pins = []
		for each in json_Obj:
			self.pins.append(each)
		#print (json_Obj)
		#print (json.dumps(aList["Keys"]).keys())
		
	def createKey(self):
		key = self.client.key.gen(type="rsa", size=4096, key_name="HydrusDB")
		return key["Id"]
	def jsonPin(self):
		self.jsonRef = self.client.add("hashTags.json", pin = True)["Hash"]
		#print (self.jsonRef)
		
	def publishChanges(self):
		publish = self.client.name.publish(self.jsonRef, key="HydrusDB")
		print ("IPNS Name is: ",publish["Name"])
class hydrusSetup():
	access_key = None
	ip = "127.0.0.1"
	port = 45869
	conf = "conf.json"
	searchParams = []
	hydrusDBLocation = None
	ipfsKey = None
	IPFSObj = IPFS()
	
	def __init__(self):

		if (os.path.exists(self.conf)):
			with open(self.conf, 'r') as myfile:
				data=myfile.read()
				obj = json.loads(data)
				#self. = str(obj[''])
				self.access_key = str(obj['access_key'])
				self.ip = str(obj['ip'])
				self.port = str(obj['port'])
				self.hydrusDBLocation = str(obj['hydrusDBLocation'])
				self.searchParams = str(obj["searchParams"]).replace("'", '"')
				self.ipfsKey = str(obj['ipfsKey'])
				myfile.close()
			self.startRunning()
		else:
			self.initialConnect()
			dison = {}
			#dison[""] = self.
			dison["access_key"] = self.access_key
			dison["ip"] = self.ip
			dison["port"] = self.port
			dison["ipfsKey"] = IPFSObj.createKey()
			print ("Please enter the search terms that you would like hydrus to automatically pin to ipfs.")
			self.searchParams = input("Comma Seperated: ")
			dison["searchParams"] = self.searchParams.split()
			print ("Please enter the absolute Location of your hydrus database. (Where Client File is.)")
			print ("Cannot use ~ to shorten /home/username/")
			self.hydrusDBLocation = input(":")
			dison["hydrusDBLocation"] = self.hydrusDBLocation
			with open(self.conf, 'w') as myfile:
				myfile.write(json.dumps(dison))
				myfile.close()
				
	def startRunning(self):	
		print ("Running Hydrus IPFS Pinner using tags:")
		print (self.searchParams)
		print ()
		
		self.searchTags()
		
		self.pinFiles()
	
		self.createJSON()
		
		self.manageJSON()
		
	def manageJSON(self):
		self.IPFSObj.jsonPin()
		self.IPFSObj.publishChanges()
	def createJSON(self):
		jsonDump = {}
	
		for each in self.IPFSHash:
			tag = self.tags[self.IPFSHash.index(each)]
			jsonDump[each] = tag
		
		if len(jsonDump) > 0:
			with open('hashTags.json', 'w') as outfile:
				json.dump(jsonDump, outfile)
	def pinFiles(self):
		notSucceed = False
		self.IPFSHash = []
		for each in self.hashes:
			if (os.path.exists(self.hydrusDBLocation + "f" + str(each[0])+ str(each[1]))):
				#print (self.hashes.index(each))
				
				self.IPFSHash.append(self.IPFSObj.addPin(self.hydrusDBLocation + "f" + str(each[0])+ str(each[1]) + "/" + str(each) + self.exts[self.hashes.index(each)])["Hash"])
				
			else:
				notSucceed = True
				
		if (notSucceed):
			print ("Could not find your files. Did you set the location correctly?")
			quit()
			
	def searchTags(self):
		ReqHeader = {'Hydrus-Client-API-Access-Key': str(self.access_key)}

		try:
			r = requests.get('http://' + str(self.ip) + ':' + self.port + '/get_files/search_files?' + '&tags=' +  
			str(urllib.parse.quote(self.searchParams, safe='')), 
				headers=ReqHeader)
			
			#print (str(self.searchParams))
			#print (r)
			#print (r.content)
		except:

			print ("Error Connecting to client: is it currently accepting API Requests?")
			print ("Go to Services -> Manage Services -> Client API and uncheck do not run client service.")
			quit()
		if (r.status_code == 409):
			print ("Client is on and not accepting API requests go to:")
			print ("Services -> Review Services -> Client API -> add -> from api request")
			quit()
		else:
			
			
			#print (str(urllib.parse.quote(str(json.loads(r.content)["file_ids"]), safe='')))
			try:
				r = requests.get('http://' + str(self.ip) + ':' + self.port + '/get_files/file_metadata?file_ids=' +  
				str(urllib.parse.quote(str(json.loads(r.content)["file_ids"]), safe='')), 
				headers=ReqHeader)
			except:
				print ("A mysterious error has occured lel")
			F = json.loads(r.content)
			f = F["metadata"]
			self.hashes = []
			self.exts = []
			self.tags = []
			for each in f:
				#print (each["hash"])
				self.hashes.append(each["hash"])
				self.exts.append(each["ext"])
				
				self.tags.append(list(each["service_names_to_statuses_to_tags"]["my tags"].values())[0])
			print ("Pulled: " + str(len(self.hashes)) + " Hashes from Hydrus.")

			return
	
	def initialConnect(self):
		ReqHeader = {'User-Agent': 'Hydrus Utilize - Mobile'}
		try:
			r = requests.get('http://' + str(self.ip) + ':' + self.port + '/request_new_permissions?' + 
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

