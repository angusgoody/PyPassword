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

To run on computers without Crypto installed use command...
pip install --use-wheel --no-index --find-links=https://github.com/sfbahr/PyCrypto-Wheels/raw/master/pycrypto-2.6.1-cp35-none-win_amd64.whl pycrypto

"""
#==================================(IMPORTS)=============================
from Crypto.Cipher import AES
import pickle
import os

from PyUi import logClass

log=logClass("Encryption Module")
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
	key=AES.new(pad(key))
	text=pad(str(plainText))
	encrypted=key.encrypt(text)
	return encrypted

def decrypt(data,key):
	try:
		key=AES.new(pad(key))
		return key.decrypt(data).rstrip()
	except:
		log.report("An error occurred when attempting to decrypt","(Decrypt)",tag="Error")

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
	log.report("Save complete exported to",fileName,tag="File")
#==================================(Classes)=============================

class dataPod:
	"""
	The data pod class is a pod
	that stores all the information
	about a account
	"""
	def __init__(self,master,podTitle):
		self.master=master
		self.podName=podTitle
		self.podVault={}
		self.edited=False

	def addData(self,name,info):
		self.podVault[name]=info
		self.edited=True

	def getVault(self):
		return self.podVault

	def getInfo(self):
		return {self.podName:self.podVault}

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

		self.edited=True

class masterPod:
	"""
	The master pod is a class
	for the pod that contains
	all the passwords for a user
	"""
	currentMasterPod=None
	currentDataPod=None
	masterPodList=[]
	def __init__(self,fileName):
		self.fileName=fileName
		self.location=fileName
		self.podDict={}
		self.masterKey=None
		masterPod.masterPodList.append(self)

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
			#Attempt unlock
			info=decrypt(content,attempt)

			#Check if decryption was successful
			try:
				info=eval(info)
			except:
				log.report("Incorrect master password used","(Unlock)",tag="File")
				return False
			else:
				log.report("Correct master password used","(Unlock)",tag="File")
				#Add key to class
				self.masterKey=attempt
				#Add all the pods to the master and return data
				podDict={}
				for iterPod in info:
					#Create pod instance
					currentPod=dataPod(self,iterPod)
					podDict[iterPod]=currentPod

					#Add the pod data
					podData=info[iterPod]
					for podSection in podData:
						currentPod.addData(podSection,podData[podSection])

					#Add the pod to self
					self.addPodRefrence(currentPod.podName,currentPod)
				return podDict
		else:
			return False

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

	def addPodRefrence(self,podTitle,podInstance):
		"""
		This method is to add pre existing pods to the master
		without returning a value
		"""
		self.podDict[podTitle]=podInstance

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
			exportDict={}
			#Gather info here
			for pod in self.podDict:

				info=self.podDict[pod].getVault()
				exportDict[pod]=info

			#Save file
			savePickle(cipher(str(exportDict),self.masterKey),self.location)

			#Update variables in pods to NOT edited
			for i in self.podDict:
				pod=self.podDict[i]
				pod.edited=False
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


#==================Testing area=================
"""
newPod=masterPod("Luigi.mp")
newPod.addKey("luigi")
gog=newPod.addPod("Google")
gog.addData("Username","angus.goody")
gog.addData("Password","frog")

git=newPod.addPod("Github")
git.addData("Username","bob.marley")
git.addData("Password","sheep56")

newPod.save()
"""

#Angus = turtle123
#Bob = secret