from tools import ethtools
from tools import web3tools


def showLockerTest(locker='0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC'):
    lockersourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(lockersourcefile)

    web3tools.showLockerContract(contractInterface, locker)


def deploy():
    # for test
    web3tools.w3 = web3tools.w3test

    ownerkey = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'

    locker = web3tools.deployContract(ownerkey)

    #showLockerTest(locker)

def showTokenBal():
    web3tools.w3 = web3tools.w3main
    tokenAddress = '0xb7cB1C96dB6B22b0D3d9536E0108d062BD488F74'
    locker = '0x5Dc9A897A7e03b30d8571231e74aC47908dE35fc'
    showLockerTest(locker)
    locker = '0x49b8402060710Aa505858F516E821Fc6dA5c234F'
    showLockerTest(locker)
    web3tools.showTokenBalance(tokenAddress, real=1)
if __name__ == '__main__':

    deploy()
    #showTokenBal()

