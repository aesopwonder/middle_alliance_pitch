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
	
#fs = cgi.FieldStorage()

#cgiUserName = str(fs.getvalue("userName"))

cgiUserName = "TestUser3"
print("Content-Type: text/html\n")
print(getUserRealName(cgiUserName, multichainSavoirObject))
