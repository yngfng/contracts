from tools import ethtools
from tools import web3tools


def showLockerTest(locker='0x2990c339470fe33f3C17E784e87e3c3f1e14BCEC'):
    lockersourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(lockersourcefile)

    web3tools.showLockerContract(contractInterface, locker)


def deploy(real=1):
    if real:
        # for real
        web3tools.w3 = web3tools.w3main

        ownerkey = '/Users/user/source/zone/Blockchain/private/fundation/w/iphone-im-w/51-distr-smn-1d72133ef711d695f74d1e2ad4830e1d592c38e7'
        tokenAddress = '0xb7cB1C96dB6B22b0D3d9536E0108d062BD488F74'
        beneficiary = [
                '0x9b2922B14f9d3286Cf9941389b764F228B97d52D',
                '0x907D4290044c176b77d0DE9C7526aeA4665d4Aaf',
                '0x34d91484307f2e1a698b247931280bd6c89b965e',
                '0x683E9560CD97b3F92EA005Cefb90E79BC2a1388A',
        ]
    else:
        # for test
        web3tools.w3 = web3tools.w3test


        ownerkey = 'accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json'
        tokenAddress = '0x554622209Ee05E8871dbE1Ac94d21d30B61013c2'
        beneficiary = [
                '0x5b21AA23A11c03b6C35A26722a8D3912C88E9c28',
                '0x73C4a7a90ebB9b02f459cF6268D2EA6e2a9161Cc',
                '0x9386d429Ab977E0C5d7eCd7aD23BD7704Ec4e0C7',
                '0xfc45bc7e9d62956A6Cd19435FfFeDD255CB66B09', ]

    name = ['smn locker 06',
            'smn locker 08',
            'smn locker 10',
            'smn locker 11',]

    releaseTimestamp = [
            ethtools.dateToTimestamp('2019-8-23 08:00:00'),
            ethtools.dateToTimestamp('2019-8-24 08:00:00'),
            ethtools.dateToTimestamp('2019-8-27 08:00:00'),
            ethtools.dateToTimestamp('2019-8-29 08:00:00'), ]
    lockers = []

    for i in [1]:
        locker = web3tools.deployLocker(ownerkey, name[i], tokenAddress, beneficiary[i], releaseTimestamp[i])
        lockers.append(locker)

    for locker in lockers:
        showLockerTest(locker)

def showTokenBal():
    web3tools.w3 = web3tools.w3main
    tokenAddress = '0xb7cB1C96dB6B22b0D3d9536E0108d062BD488F74'
    locker = '0x5Dc9A897A7e03b30d8571231e74aC47908dE35fc'
    showLockerTest(locker)
    locker = '0x49b8402060710Aa505858F516E821Fc6dA5c234F'
    showLockerTest(locker)
    web3tools.showTokenBalance(tokenAddress, real=1)
if __name__ == '__main__':

    deploy(real=0)
    #showTokenBal()

