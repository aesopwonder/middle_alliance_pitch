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


def updateRealName(userID, newRealName, savoirObject):
	newRealNameHex = convertTextToHex(newRealName)
	savoirObject.publish('realNames',userID,newRealNameHex)
	return True

fs = cgi.FieldStorage()

newNameForUpdate = fs.getvalue("TestUser3")

updateRealName("TestUser3", newNameForUpdate, multichainSavoirObject)