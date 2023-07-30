from distutils.command.upload import upload
import time,requests,random,os,base64,hashlib
from itertools import cycle
from urllib3 import connection
from json import loads
from threading import Thread

def request(self, method, url, body=None, headers=None):
    if headers is None:
        headers = {}
    else:
        headers = headers.copy()
    super(connection.HTTPConnection, self).request(method, url, body=body, headers=headers)
connection.HTTPConnection.request = request

def comment_chk(*,username,comment,levelid,percentage,type):
        part_1 = username + comment + levelid + str(percentage) + type + "xPT6iUrtws0J"
        return base64.b64encode(xor(hashlib.sha1(part_1.encode()).hexdigest(),"29481").encode()).decode()
def xor(data, key):
        return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in zip(data, cycle(key)))
def gjp_encrypt(data):
        return base64.b64encode(xor(data,"37526").encode()).decode()
def gjp_decrypt(data):
        return xor(base64.b64decode(data.encode()).decode(),"37526")

def getGJUsers(target):
    data={
        "secret":"Wmfd2893gb7",
        "str":target
    }
    request =  requests.post("http://www.boomlings.com/database/getGJUsers20.php",data=data,headers={"User-Agent": ""}).text.split(":")[1::2]
    username = request[0]
    uuid = request[2]
    accountid = request[10]
    return (username,accountid,uuid)

def uploadGJComment(name,passw,comment,perc,level):
    print("[Information]  Uploading comment...")
    try:
            accountid = getGJUsers(name)[1]                                                                                                                        
            gjp = gjp_encrypt(passw)
            c = base64.b64encode(comment.encode()).decode()
            chk = comment_chk(username=name,comment=c,levelid=str(level),percentage=perc,type="0")
            data={
                "secret":"Wmfd2893gb7",
                "accountID":accountid,
                "gjp":gjp,
                "userName":name,
                "comment":c,
                "levelID":level,
                "percent":perc,
                "chk":chk
            }
            return requests.post("http://www.boomlings.com/database/uploadGJComment21.php",data=data,headers={"User-Agent": ""}).text
    except:
            return "problem"
            
def fetchID():
    data={
        "gameVersion":"21",
        "binaryVersion":"35",
        "gdw":"0",
        "type":"4",
        "str":"",
        "diff":"-",
        "len":"-",
        "page":"0",
        "total":"0",
        "uncompleted":"0",
        "onlyCompleted":"0",
        "featured":"0",
        "original":"0",
        "twoPlayer":"0",
        "coins":"0",
        "epic":"0",
        "secret":"Wmfd2893gb7"
    }
    fetched = requests.post("http://www.boomlings.com/database/getGJLevels21.php",data=data,headers={"User-Agent": ""}).text
    return fetched.split(":")[1]

print(" /\_/\              sPYmdash v1.0")
print("( . . )            by NumbersTada")
print(">)-A-(<        Botting made easy.")
print("Based off SPAMDASH by Sevenworks.")
print("---------------------------------")
print("[Loading]      Reading config.dat")
with open("config.dat", mode="r", encoding="utf-8") as configfile:
    config=configfile.read().split(";")
    username=config[0]
    password=config[1]
    comment=config[2]
    percentage=config[3]
    interval=int(config[4])
print("[Message]      Successfully loaded.")
input("[Confirmation] Press ENTER to start commenting (using account "+username+").")

while True:
    lvlid = fetchID()
    print("[Fetching]     Fetched level ID "+lvlid)
    response = uploadGJComment(username,password,comment,percentage,lvlid)
    print("[Information]  Comment posted ("+response+")")
    time.sleep(interval/1000)
