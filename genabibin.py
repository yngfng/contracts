from tools import ethtools
from tools import web3tools
import json


if __name__ == '__main__':

    sourcefile = 'contracts/WaltonTokenLocker.sol'
    contractInterface = web3tools.compileContract(sourcefile)
    binstr = contractInterface['bin']
    abistr = contractInterface['abi']

    fbin = open('contracts/WaltonTokenLocker.bin', 'w')
    fabi = open('contracts/WaltonTokenLocker.abi', 'w')
    fbin.write(binstr)
    fabi.write(json.dumps(abistr, indent=4))


