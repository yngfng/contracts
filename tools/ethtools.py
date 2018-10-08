import time
from eth_account import Account
import getpass
import json

def genAccount():
    acct = Account.create("123456%^&*%**&*kg;djsnm,cx.ifewjqlfRTUGHJhjfgdkjas")
    keyfile = acct.encrypt("qwer1234")
    with open("accounts/{}_{}.json".format(acct.address, acct.privateKey.hex()), 'w') as fileout:
        fileout.write(json.dumps(keyfile, indent=4))

def keyfiltToPrivateKey(keyfile):
    acct = Account.decrypt(keyfile, getpass.getpass())
    #print(dir(acct))
    return acct.hex()

# timestampToDate(1566403200)
def timestampToDate(timestamp):
    timestamp = int(timestamp)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    return date

# dateToTimestamp('2018-8-29 13:24:09')
def dateToTimestamp(date):
    timestamp = time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S"))
    return int(timestamp)

if __name__ == '__main__':
    #keyfile = json.loads(open('accounts/0x18089Cb45906F19889c44c23A86b96062C245865_0xf9d8f69a65a8ede8bb26db426713eec920f73ba1e88e0a5902929c0ed140f198.json').read())
    #print(keyfiltToPrivateKey(keyfile))
    
    date = '2018-8-29 13:24:09'
    timestampe = dateToTimestamp(date)
    date2 = timestampToDate(timestampe)
    print(date, timestampe, date2)


