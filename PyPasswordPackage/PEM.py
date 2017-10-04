# coding=utf-8


#Angus Goody
#PyPassword 2.0
#02/06/17

#Password Encryption Module (PEM)

"""
PEM (Password Encryption Module)

This file is the Encryption module
this is where all the encryption and
decryption of the data will happen
to save it from being in the main __init__ file

To run on computers without Crypto installed use command...
pip install --use-wheel --no-index --find-links=https://github.com/sfbahr/PyCrypto-Wheels/raw/master/pycrypto-2.6.1-cp35-none-win_amd64.whl pycrypto

"""
#==================================(IMPORTS)=============================
from Crypto.Cipher import AES
import pickle
import os
import random
import string
from PyUi import *
import re
#==========VARIABLES=========
mainWindow=None
log=logClass("Encryption")
letters=string.ascii_letters
symbols=['!', '"', '#', '$', '%', '&', "'", '()',
         '*', '+', ',', '-', '.', '/', ':', ';',
         '<', '=', '>', '?', '@', '[', ']', '^', '_',
         '`', '{', '|', '}', '~', "'"]


#==================================(FUNCTIONS)=============================
def addPEMWindow(window):
	global mainWindow
	"""
	Allows a tk window to be added
	to this program
	"""
	mainWindow=window

def pad(text):
	"""
	For AES encryption keys and data must
	be in multiples of 16 so the pad function
	adds padding to make it the right length
	"""
	return text +((16-len(text) % 16)*"\n")

def encryptData(plainText, key):
	"""
	The cipher function encrypts
	data with an AES key
	"""
	key=AES.new(pad(key))
	text=pad(str(plainText))
	encrypted=key.encrypt(text)
	log.report("Cipher command executed","(PEM)",tag="Encryption")
	return encrypted

def decryptData(data, key):
	try:
		key=AES.new(pad(key))
		log.report("Decrypt command executed","(PEM)",tag="Encryption")
		data=key.decrypt(data).rstrip()
		try:
			data=data.decode("utf-8")
		except:
			return None
		else:
			return data
	except:
		log.report("An error occurred when attempting to decrypt","(Decrypt)",tag="Error")
		return None

def openPickle(fileName):
	"""
	This function opens a pickle file
	and returns the content
	"""
	try:
		content=pickle.load( open( fileName, "rb" ) )
	except:
		print("Error reading file")
		return None
	else:
		return content

def savePickle(content,fileName):
	"""
	This function will dump
	a pickle file
	"""
	pickle.dump(content, open( fileName, "wb" ) )
	log.report("Save complete exported to",fileName,tag="File")

def mash(length,letterList,symbolList,digitList):
	"""
	The mash function is an essential part of the
	generate password function. It mashes together all
	the random symbols and letters etc and returns
	the new password itself
	"""
	mergedList=letterList+symbolList+digitList
	mashedList=[]
	for x in range(length):
		mashedList.append(mergedList.pop(random.randint(0,len(mergedList)-1)))

	return"".join(mashedList)

def generatePassword(length,symbolAmount,digitAmount):

	"""
	This function is used to generate a password
	using the given parameters. It will generate
	the required characters then use the mash function
	to distibute the characters randomly
	"""
	#Generate letters
	charAmount=length-(symbolAmount+digitAmount)
	charList=[]
	for x in range(charAmount):
		charList.append(random.choice(letters))

	#Genetate symbols list
	symbolList=[]
	for x in range(symbolAmount):
		symbolList.append(random.choice(symbols))

	#Generate digit
	digitList=[]
	for x in range(digitAmount):
		digitList.append(str(random.randint(0,9)))


	mashed=mash(length,charList,symbolList,digitList)
	return mashed

def unlockMasterPod(masterPodInstance,attempt):
	"""
	This function will attempt to unlock a master pod using 
	an attempt. Will return True or False
	"""
	if masterPodInstance != None:
		if type(masterPodInstance) == masterPod:
			try:
				if masterPodInstance.state == "Locked":
					#Attempts to decrypt key
					decKey=decryptData(masterPodInstance.masterKey,attempt)
					if decKey != None:
						return True
					else:
						return False
				else:
					log.report("Attempted to decrypt open master pod")
					print("Err")
			except:
				log.report("An error occurred decrypting data (Invlaid pod)")
	return False

def calculatePasswordStrength(password):
	"""
	Verify the strength of 'password'
	Returns a dict indicating the wrong criteria
	A password is considered strong if:
		12 characters length or more
		1 digit or more
		1 symbol or more
		1 uppercase letter or more
		1 lowercase letter or more
	a false result means it passed
	"""

	# calculating the length
	length_error = len(password) < 11

	# searching for digits
	digit_error = re.search(r"\d", password) is None

	# searching for uppercase
	uppercase_error = re.search(r"[A-Z]", password) is None

	# searching for lowercase
	lowercase_error = re.search(r"[a-z]", password) is None

	# searching for symbols
	symbol_error = re.search(r"[ !#$%&'(@)*+,-./[\\\]^_`{|}~"+r'"]', password) is None

	# overall result
	overall = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

	results={
		'At least 12 characters' : length_error,
		'At least 1 digit' : digit_error,
		'At least 1 Uppercase' : uppercase_error,
		'At least 1 lowercase' : lowercase_error,
		'At least 1 symbol' : symbol_error,
	}

	#Track number of fails and pass
	fails=0
	success=0
	fields=len(results)
	for item in results:
		if results[item]:
			fails+=1
		else:
			success+=1
	#Return results

	return success,fails,fields,results

#==================================(Classes)=============================

class dataPod:

	"""
	The data pod class is a pod
	that stores all the information
	about a account
	"""
	def __init__(self,master,podTitle):
		#Master pod var
		self.master=master
		#Name of pod
		self.podName=podTitle
		#Stores the data
		self.podVault={}
		#Stores tags
		self.tags=[]
		#Store the type of account
		self.templateType="Login"
		#Store what state the vault is
		self.vaultState="Open"

	def addData(self,name,info):
		self.podVault[name]=info

	def updateVault(self,name,newInfo):
		"""
		This method will update the data
		pod data to the new data entered
		by the user
		"""
		#Title
		if name == "Title":
			oldName=self.podName
			self.podName=newInfo
			self.master.updatePodTitle(oldName,self.podName)
		if name in self.podVault:
			self.podVault[name]=newInfo
			log.report("Pod Vault info updated",name)
		else:
			#Add that data to the pod
			self.podVault[name]=newInfo
			log.report("New section added to pod",name,tag="File",system=True)

	def addTag(self,tagName):
		"""
		This allows the pod to have a tag
		added to it
		"""
		if tagName not in self.tags:
			self.tags.append(tagName)

	def encryptVault(self):
		"""
		This method will encrypt the data in the vault of the pod
		with the key from its master.
		"""
		if self.master.masterKey != None:
			key=self.master.masterKey
			#Encrypt all the data
			for item in self.podVault:
				oldData=self.podVault[item]
				self.podVault[item]=encryptData(oldData, key)

	def decryptVault(self):
		"""
		This method will attempt to decrypt the data in
		the vault using the master pod key.
		"""
		if self.master.masterKey != None:
			key=self.master.masterKey
			#Decrpt the data
			for item in self.podVault:
				oldData=self.podVault[item]
				self.podVault[item]=decryptData(oldData,key)

class masterPod:
	"""
	The master pod is a class
	for the pod that contains
	all the passwords for a user
	"""
	currentMasterPod=None
	currentOpenFileName=""
	masterPodDict={}
	masterPodNames=[]
	def __init__(self,fileName):
		self.masterHint="No Password Hint"
		#Stores name of master pod
		self.fileName=fileName
		#Where the file is stored
		self.location=fileName
		#Stores the pods
		self.podDict={}
		#Store the encryption key
		self.masterKey=None
		#Store what state
		self.state="Open"
		#Adds self to dictionaries
		masterPod.masterPodDict[self.location]=self
		#Stores currently loaded data pod
		currentPod=None

	def addDirectory(self,directory):
		#Updates the location of the pod
		self.location=directory
		masterPod.masterPodDict.pop(self.location,None)
		masterPod.masterPodDict[directory]=self

	def addPod(self,podName):
		"""
		This method will create a new data pod
		that contains account information
		"""
		if podName in self.podDict:
			log.report("Pod data has been overwritten",podName,tag="Pod")
		podInstance=dataPod(self,podName)
		self.podDict[podName]=podInstance
		return podInstance

	def updatePodTitle(self,oldName,newName):
		self.podDict[newName] = self.podDict.pop(oldName)

	def save(self):
		"""
		This is where the master pod
		is exported and saved to a file
		Firstly it checks all the pods
		to see if any data has been modified
		and if so then it will save to file
		"""
		#Wont save without encryption key
		if self.masterKey != None:

			#Encrypt all the pods first
			self.cipherPods()
			#Cipher key
			keyHolder=self.masterKey
			self.masterKey=encryptData(self.masterKey, self.masterKey)
			#Save file
			savePickle(self,self.location)
			#Decipher key
			self.masterKey=keyHolder
			#Decrypt the pods
			self.decryptPods()

			log.report("Saved master pod successfully","(MP)",tag="File")

		else:
			log.report("Unable to save file","(No master key)",tag="File")

	def getRootName(self):
		return os.path.splitext(self.fileName)[0]

	def deletePod(self,podName,saveOrNot):
		"""
		This method will delete a pod from the master
		by using the podName
		"""
		#Remove from dictionary
		try:
			self.podDict.pop(podName,None)
		except:
			log.report("Attempted to remove pod that isn't here",podName,tag="Error")
		else:
			log.report("Removed pod from master",podName,tag="pod")

		#Save or not
		if saveOrNot:
			self.save()

	def cipherPods(self):
		"""
		This method will encrypt all the pods
		for the master pod
		"""
		if self.state == "Open":
			for pod in self.podDict:
				#Cipher vault
				self.podDict[pod].encryptVault()
			#Update var
			self.state="Locked"

	def decryptPods(self):
		"""
		This method will decrypt all the pods
		for the master pod
		"""
		if self.state == "Locked":
			for pod in self.podDict:
				self.podDict[pod].decryptVault()
			#Update var
			self.state="Open"
#==================Testing area=================
"""
newPod=masterPod("Alan Walker.mp")
newPod.masterKey="kygo"

gog=newPod.addPod("Soundcloud")
gog.addData("Username","Alan")
gog.addData("Password","singMeToSleep123")
gog.addData("Website","soundcloud.com")
gog.templateType="Login"

bog=newPod.addPod("Spotify")
bog.addData("Username","AlanW")
bog.addData("Password","alone123")
bog.addData("Website","spotify.co.uk")
bog.addData("Notes","This is a note for spotify")
bog.templateType="Login"

noc=newPod.addPod("Ideas")
noc.templateType="Secure Note"
noc.addData("Notes","This is a note for my ideas section")

newPod.save()
"""



"""
file=openPickle("Angus.mp")
for item in file.podDict:
	pod=file.podDict[item]
	print(pod.podVault)
	for item in pod.podVault:
		print("The section name is",item,"Decrypted is",decryptData(pod.podVault[item],"turtle"))

"""
#Angus = turtle123

#Bob = secret

