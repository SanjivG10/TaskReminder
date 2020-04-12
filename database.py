import json 
import time
from encryptingDatabase import encryptDatabase,decryptDatabase

DATABASE_FILENAME='tasks.sg'

myTasksRemainder = []

#Let me read from tasks! 
try:
    with open(DATABASE_FILENAME,'rb') as f:
        msg= f.read()
        msg= decryptDatabase(msg).decode()
        if msg:
            myTasksRemainder = json.loads(msg)
except IOError:
    with open(DATABASE_FILENAME,'w' ) as f:
        jsonF = json.dumps(myTasksRemainder)
        encryptedMsg= encryptDatabase(jsonF).decode()
        f.write(encryptedMsg)
# so if file named tasks.sg is not present, I created one!

def saveDatabase():
    with open(DATABASE_FILENAME, 'w') as f:
        jsonF = json.dumps(myTasksRemainder)
        encryptedMsg= encryptDatabase(jsonF).decode()
        f.write(encryptedMsg)

def saveIntoDatabase(myTask,myTime,key=None):
    if not key:
        key = int(time.time())
    data = {}
    data[str(key)] = [myTask,myTime]
    myTasksRemainder.append(data)
    saveDatabase()
    return key 

def delDatabase(id):
    removed = False
    for index,eachVal in enumerate(myTasksRemainder):
        if removed:
            break
        for key,val in eachVal.items():
            if key==id:
                myTasksRemainder.pop(index)
                removed=True
    saveDatabase()

def getData():
    return myTasksRemainder

def updateTheListDatabase(actualKey,myTask,myTime):
    
    removed = False
    for index,eachVal in enumerate(myTasksRemainder):
        if removed:
            break
        for key,val in eachVal.items():
            if key==actualKey:
                myTasksRemainder.pop(index)
                removed=True
    saveIntoDatabase(myTask,myTime,key) 
