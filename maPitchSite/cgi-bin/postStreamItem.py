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

def convertTextToHex(textToConvert):
	bytesTextInHex = binascii.hexlify(str.encode(textToConvert))
	textInHex = str(bytesTextInHex,'ascii')
	return textInHex
	
def convertInputToString(author, title, content, address):
	authorString = "\"author\":\"" + author + "\""
	titleString = "\"title\":\"" + title + "\""
	contentString = "\"content\":\"" + content + "\""
	addressString = "\"address\":\"" + address + "\""
	outputString = "{" + authorString + "," + titleString + "," + contentString + "," + addressString + "}"
	return outputString

def generateAddress(savoirObject):
	addressString = savoirObject.getnewaddress()
	savoirObject.grant(addressString, "receive")
	return addressString

def storeStringInStream(streamName, addressForKey, stringForDef, savoirObject):
	dataHex = convertTextToHex(stringForDef)
	savoirObject.publish(streamName, addressForKey, dataHex)
	return True
	
def repPost(postAddress, savoirObject):
	txID = savoirObject.issuemore(postAddress, "maRepCoin", 1)
	return txID

def publishItemToStream(streamName, author, title, content, savoirObject):
	itemAddress = generateAddress(savoirObject)
	itemString = convertInputToString(author, title, content, itemAddress)
	itemHex = convertTextToHex(itemString)
	savoirObject.publish(streamName, itemAddress, itemHex)
	repPost(itemAddress, savoirObject)
	return itemAddress

def getUserRealName(userName, savoirObject):
	userRealNameList = savoirObject.liststreamkeyitems('realNames',userName)
	i = len(userRealNameList) - 1
	userRealNameEntry = userRealNameList[i]
	userRealNameStreamJSON = json.dumps(userRealNameEntry)
	userRealNameJSONRead = json.loads(userRealNameStreamJSON)
	userRealNameHex = userRealNameJSONRead['data']
	userRealName = convertHexAddressToString(userRealNameHex)
	return userRealName
	
def convertHexAddressToString(hexAddressToConvert):
	return bytes.fromhex(hexAddressToConvert).decode('ascii')

	
fs = cgi.FieldStorage()
cgiTitle = fs.getvalue("title")
cgiContent = fs.getvalue("content")

publishItemToStream("Marketing", getUserRealName("TestUser3",multichainSavoirObject), cgiTitle, cgiContent, multichainSavoirObject)
	
	