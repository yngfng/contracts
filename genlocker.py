import os
import time
from pprint import pprint

# releaseTime = template_releaseTimeStamp;     // template_releaseTime_human
# beneficiary = address('template_beneficiarr_address');
# string constant public name = "template_constract_name";


options = [
    {   "address":      "0x18089Cb45906F19889c44c23A86b96062C245865",
        "startdate":    "2018-08-22 0:00:00",
        "name":         "Tom",
        "iscurent":     1,
    },
]

def genContract(item):

    # setup paths
    startdate = item["startdate"]
    address = item["address"]
    name = item["name"]
    fileprefix = "smn_{}_{}_{}".format(startdate[:10], address, name)
    dirname = "../../../contracts/locker/smnlocker/"
    template = os.path.join(dirname, "template.sol")
    contract = os.path.join(dirname, fileprefix + ".sol")
    fileprefix = os.path.join(dirname, fileprefix)
    item["template"] = template
    item["contract"] = contract
    item["fileprefix"] = fileprefix

    # timestamp
    startTimestamp = time.mktime(time.strptime(startdate, "%Y-%m-%d %H:%M:%S"))
    startTimestamp = int(startTimestamp)
    releaseTimestamp = startTimestamp + 365*24*3600
    releaseDate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(releaseTimestamp))
    item["startTimestamp"] = startTimestamp
    item["releaseTimestamp"] = releaseTimestamp
    item["releaseDate"] = releaseDate
    pprint(item)

    # gen contract from template
    templateStr = open(template).read()
    templateStr = templateStr.replace("template_releaseTimeStamp", str(releaseTimestamp))
    templateStr = templateStr.replace("template_releaseTime_human", releaseDate)
    templateStr = templateStr.replace("template_beneficiarr_address", address)
    templateStr = templateStr.replace("template_constract_name", "wtc locker for " + name)

    # save contract
    with open(contract, 'w') as dataout:
        dataout.write(templateStr)

def genAbiBin(item):
    pprint(item)

    contract = item["contract"]
    binname = item["fileprefix"] + ".bin"
    abiname = item["fileprefix"] + ".abi"
    # compile
    cmd = 'solc {} --bin --abi'.format(item["contract"])
    print(cmd)

    cnt = 0
    contractName = ''
    codeType = ''
    for line in os.popen(cmd).readlines():
        print(line)
        if '======' in line:
            contractName = line.split(':')[1].split()[0]
        if 'Binary:' in line:
            cnt = 0
            codeType = 'bin'
        if 'ABI' in line:
            cnt = 0
            codeType = 'abi'
        if cnt == 1:
            #print(contractName, line[:100]),
            if contractName in ["WaltonTokenLocker"] and '====' not in line:
                if codeType == 'bin':
                    code = '0x%s' % line.strip()
                    with open(binname, 'w') as outfile:
                        outfile.write(code)
                else:
                    code = line.strip()
                    with open(abiname, 'w') as outfile:
                        outfile.write(code)
                #string = '%s%s = %s;\n' % (codeType, contractName, code)
                #outfile.write(string)
                #print(string)

        cnt += 1



def main():

    for item in options:
        # only process on iscurent==1
        if not item["iscurent"]:
            continue

        # contract
        genContract(item)

        # abi, bin, readme, run
        genAbiBin(item)
        



if __name__ == "__main__":
    main()
