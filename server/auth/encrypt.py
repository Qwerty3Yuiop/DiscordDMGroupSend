import os
import rsa
from cryptography.fernet import Fernet

def gen_keys():
    publicKey, privateKey = rsa.newkeys(512)
    return publicKey, privateKey

def fernet_encrypt(msg:str):
    fernet = Fernet(os.environ['FERNET_SECRET'])
    encrypt_msg = fernet.encrypt(msg.encode())
    return encrypt_msg

def fernet_decrypt(encrypt_msg:bytes):
    fernet = Fernet(os.environ['FERNET_SECRET'])
    msg = fernet.decrypt(encrypt_msg).decode()
    return msg

def rsa_encrypt(msg:str, pub_key:rsa.PublicKey):
    encrypt_msg = rsa.encrypt(msg.encode(), pub_key)
    return encrypt_msg

def rsa_decrypt(encrypt_msg:bytes, pri_key:rsa.PrivateKey):
    msg = rsa.decrypt(encrypt_msg, pri_key).decode()
    return msg

def rsa_to_str(key:rsa.PublicKey|rsa.PrivateKey):
    return key.save_pkcs1().decode()

def str_to_rsa_pub(key:str):
    return rsa.PublicKey.load_pkcs1(key.encode())

def str_to_rsa_pri(key:str):
    return rsa.PrivateKey.load_pkcs1(key.encode())
