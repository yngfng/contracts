from tools import ethtools
from tools import web3tools


def deployLockerTest():
    lockerkeyfile = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'
    name             = 'smn locker 1'
    tokenAddress     = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    beneficiary      = '0xfc45bc7e9d62956A6Cd19435FfFeDD255CB66B09'
    releaseTimestamp = 1566403200                                    

    web3tools.deployLocker(lockerkeyfile, name, tokenAddress, beneficiary, releaseTimestamp)

def showLockerTest():
    #showLocker()
    
    lockersourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(lockersourcefile)

    locker = '0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC'
    web3tools.showLockerContract(contractInterface, locker)

def sendTokenTest():
    keyfile = 'accounts/0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28_0x1d3f95f41e95d1f2de8e437eeb7dbb408cd4d77b2d9e92feeb1b0e9b7f777ae3.json'
    contractAddress = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    toAddress = '0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC'
    value = 123*10**18
    web3tools.sendToken(keyfile, contractAddress, toAddress, value)

if __name__ == '__main__':
    token = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
    locker = '0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC'
    ownerkey = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'
    #deployLockerTest()
    #sendTokenTest()
    web3tools.showTokenBalance(token)
    showLockerTest()

    #sendTokenTest()
    #web3tools.lockercall(ownerkey, locker, 'safeRelease')
    web3tools.lockercall(ownerkey, locker, 'release')
    #web3tools.lockercall(ownerkey, locker, 'setReleaseTime', ethtools.dateToTimestamp('2018-9-27 19:38:09'))

    web3tools.showTokenBalance(token)
    showLockerTest()

