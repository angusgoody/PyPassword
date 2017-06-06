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
	try:
		content=pickle.load( open( fileName, "rb" ) )
	except:
		return None
	else:
		return content

def savePickle(content,fileName):
	"""
	This function will dump
	a pickle file
	"""
	pickle.dump(content, open( fileName, "wb" ) )
	print("Save complete at",fileName)
#==================================(Classes)=============================

class dataPod:
	"""
	The data pod class is a pod
	that stores all the information
	about a account
	"""
	def __init__(self,podTitle,master):
		self.master=master
		self.podName=podTitle
		self.podVault={}

	def addData(self,name,info):
		self.podVault[name]=info

	def getVault(self):
		return self.podVault

	def getInfo(self):
		return {self.podName:self.podVault}

class masterPod:
	"""
	The master pod is a class
	for the pod that contains
	all the passwords for a user
	"""
	def __init__(self,fileName):
		self.location=fileName
		self.podDict={}
		self.masterKey=None

	def addKey(self,masterKey):
		self.masterKey=masterKey

	def unlock(self,attempt):
		"""
		The unlock method will attempt
		to decrypt the master pod file
		"""
		#Get file contents
		content=openPickle(self.location)
		if content != None:
			#Create encryption key
			key=AES.new(pad(attempt))
			#Attempt unlock
			info=decrypt(content,key)

			#Check if decryption was successful
			#info=eval(info)
			try:
				info=eval(info)
			except:
				print("Password incorrect")
			else:
				print("Password correct")
				print(info)
		else:
			print("Error opening file")

	def addPod(self,podName):
		"""
		This method will create a new data pod
		that contains account information
		"""
		podInstance=dataPod(podName,self)
		self.podDict[podName]=podInstance
		return podInstance

	def save(self):
		"""
		This is where the master pod
		is exported and saved to a file
		"""
		exportDict={}
		#Gather info here
		for pod in self.podDict:
			info=self.podDict[pod].getVault()
			exportDict[pod]=info

		#Encrypt file here
		encryptionKey=AES.new(pad(self.masterKey))
		#Save file
		savePickle(cipher(str(exportDict),encryptionKey),self.location)




#==================Testing area=================
