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

def convertHexNameToString(hexNameToConvert):
	return bytes.fromhex(hexNameToConvert).decode('ascii').replace("\\","")
	
def convertStringToJSON(stringToConvert):
	return json.loads(stringToConvert)

def getUserHexName(userAddress, savoirObject):
	userStreamItem = savoirObject.liststreamkeyitems('addresses',userAddress)[0]
	userStreamJSON = json.dumps(userStreamItem)
	userJSONRead = json.loads(userStreamJSON)
	userHexName = userJSONRead['data']
	return userHexName
	
def getUserRealName(userName, savoirObject):
	userRealNameList = savoirObject.liststreamkeyitems('realNames',userName)
	i = len(userRealNameList) - 1
	userRealNameEntry = userRealNameList[i]
	userRealNameStreamJSON = json.dumps(userRealNameEntry)
	userRealNameJSONRead = json.loads(userRealNameStreamJSON)
	userRealNameHex = userRealNameJSONRead['data']
	userRealName = convertHexAddressToString(userRealNameHex)
	return userRealName

def getUserNameFromAddress(userAddress, savoirObject):
	userHexName = getUserHexName(userAddress, savoirObject)
	userStringName = convertHexNameToString(userHexName)
	userRealName = getUserRealName(userStringName, savoirObject)
	return userRealName

def getAddressRepBalance(userAddress, savoirObject):
	userBalances = savoirObject.getaddressbalances(userAddress)
	userBalance = userBalances[0]['qty']
	return userBalance
	
def get3StreamItems(streamName, savoirObject):
	streamItems = savoirObject.liststreamitems(streamName, False, 3)
	streamItemArray = []
	for i in range(0,3):
		streamItem = streamItems[i]
		streamData = streamItems[i]["data"]
		streamDataString = convertHexNameToString(streamData)
		streamDataJSON = convertStringToJSON(streamDataString)
		streamDataAuthor = streamDataJSON['author']
		streamDataTitle = streamDataJSON['title']
		streamDataContent = streamDataJSON['content']
		streamDataAddress = streamDataJSON['address']
		streamOutputItem = "<b>Rep:</b> " + str(int(getAddressRepBalance(streamDataAddress, savoirObject))) + " " + "<b>Address:</b> " + streamDataAddress + " " + "<b>Author:</b> " + streamDataAuthor + "&#9;" + "<b>Title:</b> " + streamDataTitle + "&#9;&#9;" + "<b>Content:</b> " + streamDataContent
		streamItemArray.append(streamOutputItem)
	return streamItemArray
	
cgiStreamName = "Marketing"
print("Content-Type: text/html\n")
for streamItem in get3StreamItems(cgiStreamName, multichainSavoirObject):
	print(streamItem)