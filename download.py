import ipfshttpclient

import os
import json

def listToString(s): 
	str1 = ""  
    
	# traverse in the string   
	for ele in s:  
		str1 += ele + ", "   
    
	# return string   
	return str1

client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

if not os.path.exists("main.txt"):
	f = open("main.txt", "w")
	ipns = input("IPNS Hash: ")
	f.write(ipns)
	f.close()
else:
	f = open("main.txt", "r")
	ipns = f.read()
	f.close
print (ipns)
r = client.cat("/ipns/"+ipns)
#print (json.loads(r))
ipfsHash = []
ipfsDict = {}
for each in json.loads(r):
	
	ipfsDict[each] = json.loads(r)[each]
	
#print (ipfsDict)
a = open("tags.txt", "w")
for each in ipfsDict:
	print ("Downloading: " + str(each))
	client.get(each)
	a.write(str(each) + "," + listToString(ipfsDict[each]))
a.close()

