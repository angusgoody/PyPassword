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

#==================================(LISTS)=============================
#==================================(FUNCTIONS)=============================

def pad(text):
	return text +((16-len(text) % 16)*"\n")

def cipher(plainText,key):
	text=pad(plainText)
	encrypted=key.encrypt(text)
	return encrypted
#==================================(Classes)=============================
class dataPod:
	"""
	A data pod is a class which
	contains all the information about
	a certain account. It contains account name,password
	etc
	"""
	def __init__(self,podName,dataDict,master):
		self.podName=podName
		self.master=master
		self.dataDict=dataDict

class masterPod:
	"""
	The master Pod is the class that stores all
	the dataPods and is encrypted with the master
	key
	"""
	def __init__(self,masterKey):
		self.masterKey=masterKey
		self.pods={}

	def addPod(self,podName,dataDict):
		#Create pod instance
		newPod=dataPod(podName,dataDict,self)
		#Encrypt Pod
		encryptionKey=AES.new(pad(podName))
		encryptedPod=cipher(str(newPod),encryptionKey)
		#Add to master pod
		self.pods[podName]=encryptedPod

	def savePods(self,fileName):

		#Encrypt pods
		encryptionKey=AES.new(pad(self.masterKey))
		encryptedMaster=cipher(str(self.pods),encryptionKey)

		#Pickle File
		pickle.dump(encryptedMaster, open( fileName, "wb" ) )

		print("Saved pods")
	def loadPods(self,fileName):

		encryptedMaster = pickle.load( open( fileName, "rb" ) )
		encryptionKey=AES.new(pad(self.masterKey))

		decryptedPods=encryptionKey.decrypt(encryptedMaster).rstrip()
		dataDict=eval(decryptedPods)
		print(dataDict)
		

newMaster=masterPod("angus")
#newMaster.addPod("Amazon",{"Name":"Amazon","Password":"Turtle"})
#newMaster.savePods("data.p")
newMaster.loadPods("data.p")





