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

def getMakerAddress(postAddress, savoirObject):
	firstTrans = savoirObject.listaddresstransactions(postAddress,1000)[1]
	makerAddress = firstTrans['addresses'][0]
	return makerAddress

def repPost(postAddress, savoirObject):
	txID = savoirObject.issuemore(postAddress, "maRepCoin", 1)
	return txID

fs = cgi.FieldStorage()

postAddressForRep = fs.getvalue("postAddress")

repPost(postAddressForRep, multichainSavoirObject)

