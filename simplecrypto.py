import os
import base64
import Crypto.Util.number
import json
import hashlib
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

def import_key(file):
	f = open(file, 'r')
	key = RSA.importKey(f.read())
	f.close()
	return key

def aes_encrypt(plaintext, secret_key):
	# Initialization vector can be static since we're using a new secret key every time
	iv = b'\x00' * 16
	aes_handler = AES.new(secret_key, AES.MODE_CFB, iv)
	return aes_handler.encrypt(plaintext)
	
def encrypt_secret_key(rsa_key, secret_key):
	cipher = PKCS1_OAEP.new(rsa_key)
	return cipher.encrypt(secret_key)

def encrypt_data(rsa_key, input):
	secret_key = os.urandom(32)
	encrypted_secret_key = encrypt_secret_key(rsa_key, secret_key)
	encrypted_message = aes_encrypt(input, secret_key)
	return json.dumps({
		'key' : base64.b64encode(encrypted_secret_key).decode('ascii'),
		'message' : base64.b64encode(encrypted_message).decode('ascii')})
