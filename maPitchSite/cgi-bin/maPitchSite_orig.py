from Savoir import Savoir
import json

multichainRPCUser = 'multichainrpc'
multichainRPCPassword = 'test'
multichainRPCHost = '131.247.196.108'
multichainRPCPort = '2690'
multichainRPCChainName = 'maPitchChain'

multichainSavoirObject = Savoir(multichainRPCUser, multichainRPCPassword, multichainRPCHost, multichainRPCPort, multichainRPCChainName)

# Function to retrieve the user's name from the realNames blockchain stream
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

# Required header that tells the browser how to render the text.
print("Content-Type: text/html\n")

print("""<html lang="en">
<head>
  <meta charset="utf-8">

  <title>Middle Market Alliance</title>
  <meta name="description" content="Middle Alliance Crypto Landing Page">
  <meta name="author" content="Andrew Nguyen">
  <link rel="stylesheet" href="../css/stylesheet.css">
  <!--[if lt IE 9]>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html5shiv/3.7.3/html5shiv.js"></script>
  <![endif]-->
</head>

<body>
  <div id="res_wrapper" class="res_font">
    <div id="results">
      <center><h1 id="res_title">Account Information</h1></center>
    <h1 style = color:limegreen;>Public Address: <span>""" + getUserAddress("TestUser3", multichainSavoirObject) + """ </span></h1>
    <h2 style = color:limegreen;>Balance: <span>""" + str(getUserAccountBalance("TestUser3", multichainSavoirObject)) + """ maPitchCoin</span></h2>
    <h2 style = color:red;>Transaction List:
      <ul>
        <li>
          <span>Addr: 3Yu2BuptuZSiBWfr2Qy4aic6qEVnwPWasdfP0a | Amount: - 93.239</span>
        </li>
        <li>
          <span>Addr: 1Yu2BastuZSiBWfr2Qy4aic6ssqEVnasdffdHPEc | Amount: + .00123</span>
        </li>
        <li>
          <span>Addr: 1Yu2BuptasdiBWfr2Qy4aic6qEVnwPWrdkHPfg | Amount: - 9.24</span>
        </li>
        <li>
          <span>Addr: 3Yu2BuptuZSiBWfr2Qy4aic6qEVnwPWasdfP0a | Amount: + 239.22</span>
        </li>
      </ul>
    </span></h2>
    <h2><span style = color:limegreen>Name: """ + getUserRealName("TestUser3", multichainSavoirObject) + """</span><span style = color:red> - - - Reputation: 4,309 Points - - - Member Since: 2017</span></h2>

  </div>
  </div>
  <script>
</script>
</body>
</html>""")