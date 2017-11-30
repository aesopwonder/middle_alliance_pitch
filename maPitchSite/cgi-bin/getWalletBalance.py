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

def getUserAddressBalance(userAddress, savoirObject):
	if userAddress == "1Kyj1SW8JK25YyW5RaVQSCjnHQ7YUMSbxgHZX2 ":
		i = 1
	else:
		i = 0
	userBalances = savoirObject.getaddressbalances(userAddress)[i]
	userBalancesJSON = json.dumps(userBalances)
	userJSONRead = json.loads(userBalancesJSON)
	userBalance = userJSONRead['qty']
	return userBalance
	
def getUserAccountBalance(userName, savoirObject):
	userAddress = getUserAddress(userName, savoirObject)
	userAccountBalance = getUserAddressBalance(userAddress, savoirObject)
	return userAccountBalance

#fs = cgi.FieldStorage()

#cgiUserName = str(fs.getvalue("userName"))
	
cgiUserName = "TestUser3"
print("Content-Type: text/html\n")
print(getUserAccountBalance(cgiUserName, multichainSavoirObject))