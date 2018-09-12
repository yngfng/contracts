from web3 import Web3
from eth_account import Account
import getpass
from pprint import pprint
import json

def genAccount():
    acct = Account.create("123456%^&*%**&*kg;djsnm,cx.ifewjqlfRTUGHJhjfgdkjas")
    keyfile = acct.encrypt("qwer1234")
    with open("accounts/{}_{}.json".format(acct.address, acct.privateKey.hex()), 'w') as fileout:
        fileout.write(json.dumps(keyfile, indent=4))
#genAccount()
    
accts = """
0x18089Cb45906F19889c44c23A86b96062C245865
0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28
0x73C4a7a90ebB9b02f459cF6268D2EA6e2a9161Cc
0x9386d429Ab977E0C5d7eCd7aD23BD7704Ec4e0C7
0xE423410c734FE690B8966a33359B4b2AbA673E03
0xfc45bc7e9d62956A6Cd19435FfFeDD255CB66B09""".split()

w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/97ff95c5383842559ef8cfe1346ab8ba"))

# get balance
def getBalance():
    for acct in accts:
        bal = w3.eth.getBalance(acct)/10**18
        print(acct, bal)
#getBalance()

# deploy contract
def deployContract():
    print(w3.eth.gasPrice)
    print(w3.eth.getTransactionCount(accts[0]))
    signedTxn = w3.eth.account.signTransaction(dict(
            nonce=w3.eth.getTransactionCount(accts[0]),
            gasPrice=w3.eth.gasPrice,
            gas=100000,
            to=accts[1],
            value=123456789,
            data=b'',),
        "0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198"
    )
    res = w3.eth.sendRawTransaction(signedTxn.rawTransaction)
    pprint(res)
    
deployContract()

