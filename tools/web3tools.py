import web3
from web3 import Web3
from eth_account import Account
from solc import compile_source
from pprint import pprint
from tools import ethtools
from tools import web3tools
import json


# web3 instance: w3
w3test = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/97ff95c5383842559ef8cfe1346ab8ba"))
w3main = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/97ff95c5383842559ef8cfe1346ab8ba"))
w3 = w3test

gasPriceInc = 1.5
#gasPriceInc = 1

def genAcct(keyfile):
    # gen private key, then gen account instance: acct
    encrypted = json.loads(open(keyfile).read())
    privatekey = ethtools.keyfiltToPrivateKey(encrypted)
    acct = w3.eth.account.privateKeyToAccount(privatekey)
    print(acct.address)
    return acct


def compileContract(sourcefile):
    # construct contract instance: contract
    contract_source_code = open(sourcefile).read()
    compiled_sol = compile_source(contract_source_code) # Compiled source code
    contract_id, contractInterface = compiled_sol.popitem()
    return contractInterface

# top func: deploy and show locker
def deployLocker(lockerkeyfile, name, tokenAddress, beneficiary, releaseTimestamp):
    # deploy contract locker

    # keyfile to account
    acct = web3tools.genAcct(lockerkeyfile)

    # *.sol to contract interface
    lockersourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(lockersourcefile)

    # abi & bin to contract
    contract = w3.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    # form tx
    construct_txn = contract.constructor(
            name,
            tokenAddress,
            beneficiary,
            releaseTimestamp
            ).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': int(w3.eth.gasPrice*gasPriceInc) })

    # sign with acct, then send raw transaction
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    # waiting for receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    pprint(tx_receipt)

    # get address of contract
    contractAddress = tx_receipt.get('contractAddress')
    print('contractAddress contract address is : ', contractAddress)
    #web3tools.showLockerContract(contractInterface, contractAddress)
    return contractAddress

# top func: deploy and show contract
def deployContract(keyfile):
    # deploy contract

    # keyfile to account
    acct = web3tools.genAcct(keyfile)

    # *.sol to contract interface
    lockersourcefile = 'contracts/WaltonToken.sol'
    contractInterface = web3tools.compileContract(lockersourcefile)

    # abi & bin to contract
    contract = w3.eth.contract(abi=contractInterface['abi'], bytecode=contractInterface['bin'])
    # form tx
    construct_txn = contract.constructor().buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': int(w3.eth.gasPrice*gasPriceInc) })

    # sign with acct, then send raw transaction
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    # waiting for receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    pprint(tx_receipt)

    # get address of contract
    contractAddress = tx_receipt.get('contractAddress')
    print('contractAddress contract address is : ', contractAddress)
    #web3tools.showLockerContract(contractInterface, contractAddress)
    return contractAddress


def showLockerContract(contractInterface, contractAddress):
    contractOnline = w3.eth.contract(abi=contractInterface['abi'], address=contractAddress)
    releaseTimestamp = contractOnline.functions.releaseTimestamp().call()
    currentTimestamp = contractOnline.functions.currentTimestamp().call()
    secondsRemaining = contractOnline.functions.secondsRemaining().call()
    tokenLocked = contractOnline.functions.tokenLocked().call()
    print(
        '\n'
        '---------------------------------------------------------------\n'
        'contract information: \n'
        '-----------------+---------------------------------------------\n'
        'owner            | {}\n'
        'contractAddress  | {}\n'
        'name             | {}\n'
        'token            | {}\n'
        'beneficiary      | {}\n'
        'tokenLocked      | {}\n'
        '-----------------+---------------------------------------------\n'
        'releaseTimestamp | {:<20} {}\n'
        'currentTimestamp | {:<20} {}\n'
        'secondsRemaining | {:<20} {} days\n'
        '-----------------+---------------------------------------------\n'.format(
        contractOnline.functions.owner().call(),
        contractAddress,
        contractOnline.functions.name().call(),
        contractOnline.functions.token().call(),
        contractOnline.functions.beneficiary().call(),
        tokenLocked/10**18,

        releaseTimestamp, ethtools.timestampToDate(releaseTimestamp),
        currentTimestamp, ethtools.timestampToDate(currentTimestamp),
        secondsRemaining, secondsRemaining/3600/24,
        ))

def sendToken(keyfile, contractAddress, toAddress, value):
    # gen acct
    acct = web3tools.genAcct(keyfile)

    # gen contract interface
    sourcefile = 'contracts/WaltonToken.sol'
    contractInterface = web3tools.compileContract(sourcefile)

    contractOnline = w3.eth.contract(abi=contractInterface['abi'], address=contractAddress)

    # form tx
    construct_txn = contractOnline.functions.transfer(toAddress, value).buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': int(w3.eth.gasPrice*gasPriceInc) })

    # sign with acct, then send raw transaction
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    # waiting for receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    pprint(tx_receipt)
    return tx_receipt

def lockercall(keyfile, contractAddress, func, releaseTime=1566403200):
    # gen acct
    acct = web3tools.genAcct(keyfile)

    # gen contract interface
    sourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(sourcefile)

    contractOnline = w3.eth.contract(abi=contractInterface['abi'], address=contractAddress)

    # form tx
    if func == 'release':
        contractFunc = contractOnline.functions.release()
    elif func == 'safeRelease':
        contractFunc = contractOnline.functions.safeRelease()
    elif func == 'setReleaseTime':
        contractFunc = contractOnline.functions.setReleaseTime(int(releaseTime))

    construct_txn = contractFunc.buildTransaction({
        'from': acct.address,
        'nonce': w3.eth.getTransactionCount(acct.address),
        'gas': 1728712,
        'gasPrice': int(w3.eth.gasPrice*gasPriceInc) })

    # sign with acct, then send raw transaction
    signed = acct.signTransaction(construct_txn)
    tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)

    # waiting for receipt
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    pprint(tx_receipt)
    return tx_receipt

def showTokenBalance(contractAddress, real=0):
    # gen contract interface
    sourcefile = 'contracts/WaltonToken.sol'
    contractInterface = web3tools.compileContract(sourcefile)

    contractOnline = w3.eth.contract(abi=contractInterface['abi'], address=contractAddress)
    name = contractOnline.functions.name().call()
    symbol = contractOnline.functions.symbol().call()
    decimals = contractOnline.functions.decimals().call()
    totalSupply = contractOnline.functions.totalSupply().call()

    print(
        '\n'
        '---------------------------------------------------------------\n'
        'token information: \n'
        '-----------------+---------------------------------------------\n'
        'contractAddress  | {}\n'
        'name             | {}\n'
        'symbol           | {}\n'
        'decimals         | {}\n'
        'totalSupply      | {:,}\n'
        '-----------------+---------------------------------------------'.format(
        contractAddress,
        name,
        symbol,
        decimals,
        totalSupply/10**18 ))

    if real:
        addresses = [
                '0xD93fB95dA2148BF3cb1d30d7498B447bC240F3D7',
                '0xc2c4CE063aF8f547E596b6Fa3771Bf423D495817',
                '0xC04608b9d32F74D88b40e837DA740B297E2940Ab',
                '0xCCd8e06861943fDaBf413628F272d21Bd0E08EDB',
                '0x01677C56443Fb9537Bf6481a86502a4fF5C995c7',
                '0x9b2922B14f9d3286Cf9941389b764F228B97d52D',
                '0xD1cE4C4ad8770824b068848dD36c05b0b74F28Ec',
                '0x907D4290044c176b77d0DE9C7526aeA4665d4Aaf',
                '0x020675cd807d796f4e676ec76b3A162988052020',
                '0x34D91484307F2e1A698b247931280Bd6c89B965e',
                '0x683E9560CD97b3F92EA005Cefb90E79BC2a1388A', ]
    else:
        addresses = [
                '0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC',
                '0x18089Cb45906F19889c44c23A86b96062C245865',
                '0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28',
                '0x73C4a7a90ebB9b02f459cF6268D2EA6e2a9161Cc',
                '0x9386d429Ab977E0C5d7eCd7aD23BD7704Ec4e0C7',
                '0xE423410c734FE690B8966a33359B4b2AbA673E03',
                '0xfc45bc7e9d62956A6Cd19435FfFeDD255CB66B09' ]

    print('     address                                  |  balance')
    print('----------------------------------------------+----------------')
    for owner in addresses:
        bal = contractOnline.functions.balanceOf(owner).call()
        print('{}    |    {:<12,}'.format(owner, bal/10**18))

    print('----------------------------------------------+----------------\n')


if __name__ == '__main__':

    # deploy contract locker
    lockerkeyfile = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'
    acct = genAcct(lockerkeyfile)

    lockersourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = compileContract(lockersourcefile)

    name             = 'smn locker 1'
    tokenAddress     = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    beneficiary      = acct.address
    releaseTimestamp = 1566403200                                    
                        
    tx_receipt = deployContract(
            contractInterface,
            acct,
            name,
            tokenAddress,
            beneficiary,
            releaseTimestamp
        )
    locker = tx_receipt.get('contractAddress')
    print('locker is : ', locker)
    showLockerContract(contractInterface, locker)

    # deploy Token
    #tokenkeyfile = 'accounts/0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28_0x1d3f95f41e95d1f2de8e437eeb7dbb408cd4d77b2d9e92feeb1b0e9b7f777ae3.json'
    #tokensourcefile = 'contracts/WaltonToken.sol'

    # Token
    #token = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    #locker = '0xAbb11084F2657d19B730A33c08bFE1ae5C5E3C2C'

    #tokencont = Contract(tokenkeyfile, tokensourcefile)




