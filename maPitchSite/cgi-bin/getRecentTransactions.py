from Savoir import Savoir
import json
import binascii
import sys
import cgi


multichainRPCUser = 'multichainrpc'
multichainRPCPassword = 'test'
multichainRPCHost = '131.247.196.108'
multichainRPCPort = '2690'
multichainRPCChainName = 'maPitchChain'

multichainSavoirObject = Savoir(multichainRPCUser, multichainRPCPassword, multichainRPCHost, multichainRPCPort, multichainRPCChainName)

def getUserHexAddress(userName, savoirObject):
	userStreamItem = savoirObject.liststreamkeyitems('users',userName)[0]
	userStreamJSON = json.dumps(userStreamItem)
	userJSONRead = json.loads(userStreamJSON)
	userHexAddress = userJSONRead['data']
	return userHexAddress

def convertHexAddressToString(hexAddressToConvert):
	return bytes.fromhex(hexAddressToConvert).decode('ascii')
	
def getUserAddress(userName, savoirObject):
	userHexAddress = getUserHexAddress(userName, savoirObject)
	userAddress = convertHexAddressToString(userHexAddress)
	return userAddress

def get3Transactions(userName, savoirObject):
	userAddress = getUserAddress(userName, savoirObject)
	userTransItems = savoirObject.listaddresstransactions(userAddress,3)
	userTransArray = []
	for i in range(0,3):
		transaction = userTransItems[i]
		transItemForOutputArray = ""
		transItemForOutputArray += str(transaction['balance']['assets'][0]['name'])
		transItemForOutputArray += "&#9;" + str(transaction['balance']['assets'][0]['qty'])
		transItemForOutputArray += "&#9;" + str(transaction['addresses'][0])
		userTransArray.append(transItemForOutputArray)
	return userTransArray
	
cgiUserName = "TestUser3"
print("Content-Type: text/html\n")
for transaction in get3Transactions(cgiUserName, multichainSavoirObject):
	print(transaction)
