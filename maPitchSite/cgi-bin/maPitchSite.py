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

print("""
	<head>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
	<script>
		$(document).ready(function(){
    $("#updateName").click(function(){
		var newName = prompt("Update your name:", "Enter new name here");
        $.ajax({
			url: "updateName.py",
			type: "post",
			datatype:"json",
			data: {'TestUser3' : newName}
			});
		});
	$("#sendCoins").click(function(){
		var recipientName = prompt("Enter recipient username:");
		var coinName = prompt("Enter coin name:");
		var coinAmount = prompt("Enter number of coins to send:");
		var privKey = prompt("Sending " + coinAmount + " " + coinName + " to " + recipientName + "...", "Enter Private Key To Confirm");
        $.ajax({
			url: "sendCoinToUser.py",
			type: "post",
			datatype:"json",
			data: {'userName' : "TestUser3", 'recipientName' : recipientName, 'coinName' : coinName, 'coinAmount' : coinAmount, 'privKey' : privKey}
			});
		});
	});
	
	</script>
	</head>
	<body>
    <p><b>Name:</b> """ + getUserRealName("TestUser3", multichainSavoirObject) + """&nbsp&nbsp&nbsp&nbsp<button type="button" class="btn" id="updateName">Update</button></p>
	<p><b>Wallet balance:</b> """ + str(getUserAccountBalance("TestUser3", multichainSavoirObject)) + """&nbsp&nbsp&nbsp&nbsp<button type="button" class="btn" id="sendCoins">Send Coins</button></p>
	</body>
	""")