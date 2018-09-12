import web3
from web3 import Web3
from eth_account import Account
from solc import compile_source
from pprint import pprint
import ethtools
import json


class Contract:
    def __init__(self, keyfile, sourcefile):

        # web3 instance: w3
        self.w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/97ff95c5383842559ef8cfe1346ab8ba"))

        # gen private key, then gen account instance: acct
        encrypted = json.loads(open(keyfile).read())
        privatekey = ethtools.keyfiltToPrivateKey(encrypted)
        self.acct = self.w3.eth.account.privateKeyToAccount(privatekey)
        print(self.acct.address)

        # construct contract instance: contract
        contract_source_code = open(sourcefile).read()
        compiled_sol = compile_source(contract_source_code) # Compiled source code
        contract_id, contract_interface = compiled_sol.popitem()
        self.contract_interface = contract_interface
        self.contract = self.w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    def deployContract(self):
        # form tx
        construct_txn = self.contract.constructor().buildTransaction({
            'from': self.acct.address,
            'nonce': self.w3.eth.getTransactionCount(self.acct.address),
            'gas': 1728712,
            'gasPrice': self.w3.eth.gasPrice })

        # sign with acct, then send raw transaction
        signed = self.acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)

        # waiting for receipt
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        pprint(tx_receipt)
        return tx_receipt

    def sendToken(self, contractAddress, toAddress, value):
        contractOnline = self.w3.eth.contract(abi=self.contract_interface['abi'], address=contractAddress)

        # form tx
        construct_txn = contractOnline.functions.transfer(toAddress, value).buildTransaction({
            'from': self.acct.address,
            'nonce': self.w3.eth.getTransactionCount(self.acct.address),
            'gas': 1728712,
            'gasPrice': self.w3.eth.gasPrice })

        # sign with acct, then send raw transaction
        signed = self.acct.signTransaction(construct_txn)
        tx_hash = self.w3.eth.sendRawTransaction(signed.rawTransaction)

        # waiting for receipt
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        pprint(tx_receipt)
        return tx_receipt



    def showTokenContract(self, contractAddress):
        contractOnline = self.w3.eth.contract(abi=self.contract_interface['abi'], address=contractAddress)
        name = contractOnline.functions.name().call()
        symbol = contractOnline.functions.symbol().call()
        decimals = contractOnline.functions.decimals().call()
        totalSupply = contractOnline.functions.totalSupply().call()
        print(' name           {}\n symbol         {}\n decimals       {}\n totalSupply    {:,}\n'.format(name, symbol, decimals, totalSupply/10**18))

    def showLockerContract(self, contractAddress):
        contractOnline = self.w3.eth.contract(abi=self.contract_interface['abi'], address=contractAddress)
        releaseTimestamp = contractOnline.functions.releaseTimestamp().call()
        currentTimestamp = contractOnline.functions.currentTimestamp().call()
        secondsRemaining = contractOnline.functions.secondsRemaining().call()
        tokenLocked = contractOnline.functions.tokenLocked().call()
        print(
            'releaseTimestamp: {} {}\n'
            'currentTimestamp: {} {}\n'
            'secondsRemaining: {} {} days\n'
            'tokenLocked     : {}\n'.format(
            releaseTimestamp, ethtools.timestampToDate(releaseTimestamp),
            currentTimestamp, ethtools.timestampToDate(currentTimestamp),
            secondsRemaining, secondsRemaining/3600/24,
            tokenLocked     ))

    def balanceOf(self, contractAddress, owner):
        contractOnline = self.w3.eth.contract(abi=self.contract_interface['abi'], address=contractAddress)
        #bal = contractOnline.functions.name().call()
        bal = contractOnline.functions.balanceOf(owner).call()
        print('{} - balance: {:,}'.format(owner, bal/10**18))

if __name__ == '__main__':
    # deploy Token
    tokenkeyfile = 'accounts/0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28_0x1d3f95f41e95d1f2de8e437eeb7dbb408cd4d77b2d9e92feeb1b0e9b7f777ae3.json'
    tokensourcefile = '../../../contracts/WaltonToken.sol'

    # deploy locker
    lockerkeyfile = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'
    lockersourcefile = '../../../contracts/locker/smnlocker/smn_2018-08-22_0x18089Cb45906F19889c44c23A86b96062C245865_Tom.sol'

    # Token
    token = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    locker = '0xAbb11084F2657d19B730A33c08bFE1ae5C5E3C2C'

    tokencont = Contract(tokenkeyfile, tokensourcefile)
    lockercont = Contract(lockerkeyfile, lockersourcefile)


    #tokencont.deployContract()
    #lockercont.deployContract()
    tokencont.sendToken(token, locker, 5000*10**18)
    tokencont.showTokenContract(token)
    lockercont.showLockerContract(locker)
    tokencont.balanceOf(token, '0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28')


