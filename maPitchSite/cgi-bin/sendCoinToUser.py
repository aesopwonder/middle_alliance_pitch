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
	
def createTransaction(userName, recipientName, coinName, qty, savoirObject):
	senderAddress = getUserAddress(userName, savoirObject)
	recipientAddress = getUserAddress(recipientName, savoirObject)	
	txIDHex = savoirObject.createrawsendfrom(senderAddress, {recipientAddress : {coinName : int(qty)}})
	return txIDHex
	
def signTransaction(rawTransactionIDHex, midArray, privKeyArray, savoirObject):
	txIDJSON = json.dumps(savoirObject.signrawtransaction(rawTransactionIDHex, midArray, privKeyArray))
	txIDRead = json.loads(txIDJSON)
	txIDHex = txIDRead['hex']
	return txIDHex

def sendTransaction(signedTransactionIDHex, savoirObject):
	txIDHex = savoirObject.sendrawtransaction(signedTransactionIDHex)
	return txIDHex

def sendCoinsToUser(userName, recipientUserName, coinName, amount, privKey, savoirObject):
	createTransactionID = createTransaction(userName, recipientUserName, coinName, amount, savoirObject)
	signTransactionID = signTransaction(createTransactionID, [], [privKey], savoirObject)
	sendTransactionID = sendTransaction(signTransactionID, savoirObject)
	return sendTransactionID
	
fs = cgi.FieldStorage()
cgiUserName = fs.getvalue("userName")
cgiRecipientName = fs.getvalue("recipientName")
cgiCoinName = fs.getvalue("coinName")
cgiAmount = fs.getvalue("coinAmount")
cgiPrivKey = fs.getvalue("privKey")

print("Test")

sendCoinsToUser(cgiUserName, cgiRecipientName, cgiCoinName, cgiAmount, cgiPrivKey, multichainSavoirObject)
