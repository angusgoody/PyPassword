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

def chiper(plainText, key):
	"""
	The cipher function encrypts
	data with an AES key
	"""
	text=pad(str(plainText))
	encrypted=key.encrypt(text)
	return encrypted

def decrypt(data,key):
	return key.decrypt(data).rstrip()

#==================================(Classes)=============================
class dataPod:
	"""
	A data pod is a class which
	contains all the information about
	a certain account. It contains account name,password
	etc
	"""
	def __init__(self,podName,podVault,master):
		self.podName=podName
		self.master=master
		self.podVault=chiper(podVault,self.master.masterKey)

	def __string__(self):
		return self.podName

	def getPodData(self):
		"""
		This method returns just the data inside the pod
		which is known as the pod vault and contains the
		private information
		"""
		return self.podVault

	def getPod(self):
		"""
		This method returns a dictionary which
		contains the podName and podVault
		"""
		return {self.podName:self.podVault}


class masterPod:
	"""
	The master Pod is the class that stores all
	the dataPods and is encrypted with the master
	key
	"""
	def __init__(self,masterKey):
		#Create an AES encryption key
		self.masterKey=AES.new(pad(masterKey))
		self.pods={}

	def addPod(self,podName,dataDict):
		"""
		The add pod function will create
		a dataPod with the master pod
		as the master and add it to the master pod
		collection
		"""
		#Create pod instance
		newPod=dataPod(podName,dataDict,self)
		newPodData=newPod.getPodData()
		#Add to master pod
		self.pods[podName]=newPodData

	def savePods(self,fileName):
		"""
		The save pods method will encrypt the dictionary
		that contains all the pods and export it to a file
		using Pickle
		"""

		#Encrypt pods
		encryptedMaster=chiper(str(self.pods), self.masterKey)

		#Pickle File
		pickle.dump(encryptedMaster, open( fileName, "wb" ) )

		print("Saved pods")
	def loadPods(self,fileName):

		encryptedMaster = pickle.load( open( fileName, "rb" ) )
		decryptedPods=self.masterKey.decrypt(encryptedMaster).rstrip()
		dataDict=eval(decryptedPods)
		print(dataDict)


newMaster=masterPod("angus")
#newMaster.addPod("Amazon",{"Name":"Amazon","Password":"Turtle"})
#newMaster.savePods("data.p")
newMaster.loadPods("data.p")


