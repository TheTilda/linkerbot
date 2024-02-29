
from cryptography.fernet import Fernet
 
# we will be encrypting the below string.
message = "hello geeks"
 
# generate a key for encryption and decryption
# You can use fernet to generate 
# the key or use random key generator
# here I'm using fernet to generate key

def gen_key():
    key = Fernet.generate_key()
    f = open('public.txt', 'wb')
    f.write(key)
    f.close()

def crypt(message):
    f = open("public.txt", 'rb')
    key = f.read()
    fernet = Fernet(key)
    encMessage = fernet.encrypt(message.encode())
    
    return encMessage.decode("utf-8")

def encrypt(message):
    f = open('public.txt', 'rb')
    key = f.read()
    fernet = Fernet(key)
    decMessage = fernet.decrypt(message).decode()
    return decMessage


