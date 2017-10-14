from Savoir import Savoir
import json

from Savoir import Savoir
multichainRPCUser = 'multichainrpc'
multichainRPCPassword = 'test'
multichainRPCHost = <IP ADDRESS>
multichainRPCPort = <PORT>
multichainRPCChainName = 'maPitchChain'

multichainSavoirObject = Savoir(multichainRPCUser, multichainRPCPassword, multichainRPCHost, multichainRPCPort, multichainRPCChainName)

def getUserAddressBalance(userAddress, savoirObject):
	userBalances = savoirObject.getaddressbalances(userAddress)[0]
	userBalancesJSON = json.dumps(userBalances)
	userJSONRead = json.loads(userBalancesJSON)
	userBalance = userJSONRead['qty']
	return userBalance

def convertHexAddressToString(hexAddressToConvert):
	return bytes.fromhex(hexAddressToConvert).decode('ascii')
	
def getUserHexAddress(userName, savoirObject):
	userStreamItem = savoirObject.liststreamkeyitems('users',userName)[0]
	userStreamJSON = json.dumps(userStreamItem)
	userJSONRead = json.loads(userStreamJSON)
	userHexAddress = userJSONRead['data']
	return userHexAddress

def getUserAddress(userName, savoirObject):
	userHexAddress = getUserHexAddress(userName, savoirObject)
	userAddress = convertHexAddressToString(userHexAddress)
	return userAddress
	
def getUserAccountBalance(userName, savoirObject):
	userAddress = getUserAddress(userName, savoirObject)
	userAccountBalance = getUserAddressBalance(userAddress, savoirObject)
	return userAccountBalance
	
