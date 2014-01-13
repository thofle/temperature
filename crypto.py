import os
import Crypto.Util.number
from Crypto.Cipher import DES3
from Crypto.PublicKey import RSA


CRYPTO_SYMMETRIC_KEY_LENGTH = 24


def import_key(file):
	f = open(file, 'r')
	key = RSA.importKey(f.read())
	f.close()
	return key

def generate_key():
	return RSA.generate(4096)

def save_public_key(file, key):
	f = open(file,'wb')
	f.write(key.publickey().exportKey())
	f.close()
	
def save_private_key(file, key):
	f = open(file,'wb')
	f.write(key.exportKey('PEM'))
	f.close()
	
def des_encrypt(plaintext, secret_key):
	# Initialization vector can be static since we're using a new secret key every time
	iv = b'\xe3' * 8
	des_handler = DES3.new(secret_key, DES3.MODE_CFB, iv)
	return des_handler.encrypt(plaintext)
	
def des_decrypt(encrypted_text, secret_key):
	iv = b'\xe3' * 8
	des_handler = DES3.new(secret_key, DES3.MODE_CFB, iv)
	return des_handler.decrypt(encrypted_text)
	
def encrypt_secret_key(rsa_key, secret_key):
	plaintext_length = (Crypto.Util.number.size(rsa_key.n) - 2) / 8
	padding = b'\xff' + os.urandom(24)
	padding += b'\x00' * int(plaintext_length - len(padding) - len(secret_key))
	encrypted_secret_key = rsa_key.encrypt(padding + secret_key, None)
	return encrypted_secret_key[0]
	
def decrypt_secret_key(rsa_key, encrypted_secret_key):
	decrypted = rsa_key.decrypt(encrypted_secret_key)
	secret_key = decrypted[(511 - CRYPTO_SYMMETRIC_KEY_LENGTH):]
	return bytes(secret_key)
	
secret_key = os.urandom(CRYPTO_SYMMETRIC_KEY_LENGTH)
encrypted_secret_key = encrypt_secret_key(key, secret_key)
encrypted_message = des_encrypt('super secret message', secret_key)
