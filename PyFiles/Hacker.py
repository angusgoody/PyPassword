
from Tkinter import *
import pickle
from Crypto.Cipher import AES
from Tkinter import filedialog
import PEM

window=Tk()
window.geometry("400x300")

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
	return encrypted

def decryptData(data, key):
	try:
		key=AES.new(pad(key))
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

		
def run():
	#Gather
	passwords=[]
	fileToOpen=filedialog.askopenfilename(filetypes=(("Master Pod", "*.mp"),
	                                           ("All files", "*.*")))
	dataClass=pickle.load( open( fileToOpen, "rb" ) )
	attempt=input("Enter password attempt: ")
	if type(dataClass) == PEM.masterPod:
		print("Searching:",fileToOpen)
		for item in dataClass.podDict:
			#Get the pods
			pod=dataClass.podDict[item]
			for section in pod.podVault:
				info=decryptData(pod.podVault[section], attempt)
				if info != None:
					passwords.append(info)
	
	print("Passwords retrieved are",passwords)
					
	
mainButton=Button(window,text="Scan",command=run)
mainButton.pack(expand=True)
window.mainloop()