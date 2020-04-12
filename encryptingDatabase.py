import cryptography
from cryptography.fernet import Fernet
import json 

KEY_FILENAME= 'encrypt.key'

#saving json file check! 



try:
    with open(KEY_FILENAME,'r') as f:
        key= f.read()
except IOError:
    with open(KEY_FILENAME,'w') as f:
        key = Fernet.generate_key().decode()
        f.write(key)

def encryptDatabase(message,saveDatabaseBool=False):
    # get the message in bytes
    message= message.encode()
    f = Fernet(key)
    encryptedMessage = f.encrypt(message)
    return encryptedMessage

def decryptDatabase(encryptedMessage):
    f = Fernet(key)
    return f.decrypt(encryptedMessage)


