# coding=utf-8


#Angus Goody
#PyPassword 2.0
#02/06/17

#Password Encryption Module (PEM)

"""
This file is the Encryption module
this is where all the encryption and
decryption of the data will happen
to save it from being in the main __init__ file
"""
#==================================(IMPORTS)=============================
from Crypto.Cipher import AES
import pickle

#==================================(FUNCTIONS)=============================

def pad(text):
	"""
	For AES encryption keys and data must
	be in multiples of 16 so the pad function
	adds padding to make it the right length
	"""
	return text +((16-len(text) % 16)*"\n")

def cipher(plainText, key):
	"""
	The cipher function encrypts
	data with an AES key
	"""
	text=pad(str(plainText))
	encrypted=key.encrypt(text)
	return encrypted

def decrypt(data,key):
	return key.decrypt(data).rstrip()

def openPickle(fileName):
	"""
	This function opens a pickle file
	and returns the content
	"""
	content=pickle.load( open( fileName, "rb" ) )
	return content
#==================================(Classes)=============================

class dataPod:
	"""
	The data pod class is a pod
	that stores all the information
	about a account
	"""
	def __init__(self):
		pass
class masterPod:
	"""
	The master pod is a class
	for the pod that contains
	all the passwords for a user
	"""
	def __init__(self,fileName):
		self.location=fileName

	def unlock(self,attempt):
		"""
		The unlock method will attempt
		to decrypt the master pod file
		"""
		#Get file contents
		try:
			content=openPickle(self.location)
		except:
			print("Could not find specified path")
		else:
			#Create encryption key
			key=AES.new(pad(attempt))
			#Attempt unlock
			info=decrypt(content,key)

			#Check if decryption was successful

	def addPod(self):
		pass




