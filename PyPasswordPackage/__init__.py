# coding=utf-8


#Angus Goody
#PyPassword 2.0
#02/06/17

#Main Init File

#===============================(IMPORTS)===============================
from tkinter import *
from tkinter import messagebox
import random
import os

from PyUi import *
from PEM import *

#===============================(WINDOW SETUP)===============================
window=Tk()
window.title("PyPassword 2")
window.geometry("400x300")

#---Main Menu---
mainMenu=Menu(window)

fileMenu=Menu(mainMenu)
editMenu=Menu(mainMenu)
viewMenu=Menu(mainMenu)

#---Lock Screen Menu---
lockScreenMenu=Menu(window)

#--Status bar--
statusVar=StringVar()
statusBar=mainFrame(window)
statusBar.pack(fill=X,side=BOTTOM)
statusLabel=mainLabel(statusBar,textvariable=statusVar)
statusLabel.pack(expand=True)

#===============================(VARIABLES/ARRAYS)===============================
currentDirectory=os.getcwd()
lockedScreens=[]
#===============================(USER INTERFACE)===============================

#-----Open Screen----
# region open screen
openScreen=mainScreen(window,"PyPassword",statusVar,menu=lockScreenMenu)
lockedScreens.append(openScreen)
openScreen.show()

#--Top--
openTopVar=StringVar()
openTopVar.set("Select Pod Or Create New One")
openTopFrame=topStrip(openScreen,openTopVar)
openTopFrame.pack(side=TOP,fill=X)

#--Main--
openMainFrame=mainFrame(openScreen)
openMainFrame.pack(expand=True,fill=BOTH)

openMainListbox=advancedListbox(openMainFrame,font="courier 19")
openMainListbox.pack(expand=True,fill=BOTH)

#--Bottom--
openBottomFrame=mainFrame(openScreen)
openBottomFrame.pack(fill=X,side=BOTTOM)

openBottomButtonFrame=mainFrame(openBottomFrame)
openBottomButtonFrame.pack(expand=True)

openCreateFileButton=mainButton(openBottomButtonFrame,text="Create Master Pod",width=12)
openCreateFileButton.pack(side=LEFT,padx=5)
openSelectFileButton=mainButton(openBottomButtonFrame,text="Open Selected",width=12)
openSelectFileButton.pack(side=RIGHT,padx=5)

#endregion

#----Open Master Password Screen-----
#region master screen
openMasterScreen=mainScreen(window, "Master Password", statusVar,menu=lockScreenMenu)
lockedScreens.append(openMasterScreen)

openMasterDisplay=displayView(openMasterScreen)
openMasterDisplay.pack(expand=True,fill=BOTH)

#--Top Section--
openMasterTopFrame=centerFrame(openMasterDisplay)
openMasterSub=openMasterTopFrame.miniFrame

titleLabel(openMasterSub,text="File: ").pack(side=LEFT)
openMasterTopVar=StringVar()
openMasterTopVar.set("None")
titleLabel(openMasterSub,textvariable=openMasterTopVar).pack(side=RIGHT)

#--Main Section--
openMasterMainFrame=centerFrame(openMasterDisplay)
openMasterSub=openMasterMainFrame.miniFrame

mainLabel(openMasterSub,text="Enter password").pack()
openMasterEntry=Entry(openMasterSub,show="•",justify=CENTER)
openMasterEntry.pack()

#--Bottom Section--
openMasterBottomFrame=centerFrame(openMasterDisplay)
openMasterBottomSub=openMasterBottomFrame.miniFrame

openMasterUnlockButton=Button(openMasterBottomSub,text="Unlock",width=12)
openMasterUnlockButton.pack(pady=5)
openMasterCancelButton=Button(openMasterBottomSub,text="Cancel",width=12)
openMasterCancelButton.pack()

#--Add Views--
openMasterDisplay.addSection(openMasterTopFrame)
openMasterDisplay.addSection(openMasterMainFrame)
openMasterDisplay.addSection(openMasterBottomFrame)

openMasterDisplay.showSections()

#endregion

#----Home screen-----
#region home screen
homeScreen=mainScreen(window,"Home",statusVar,menu=mainMenu)

#Main view
homeMainFrame=mainFrame(homeScreen)
homeMainFrame.pack(expand=True,fill=BOTH)

homePodListbox=advancedListbox(homeMainFrame,font="Arial 18")
homePodListbox.pack(expand=True,fill=BOTH)

#Bottom View
homeBottomFrame=centerFrame(homeScreen)
homeBottomFrame.pack(side=BOTTOM,fill=X)
homeBottomSub=homeBottomFrame.miniFrame

homeOpenPodButton=Button(homeBottomSub,text="Open Pod",width=9)
homeOpenPodButton.pack()

homeNewPodButton=Button(homeBottomSub,text="New Pod",width=9)
homeNewPodButton.pack(pady=5)
#endregion

#---View Pod Screen---
viewPodScreen=mainScreen(window,"Pod Info",statusVar)

#Top Bar
viewPodTopFrame=centerFrame(viewPodScreen)
viewPodTopFrame.pack(side=TOP,fill=X)
viewPodTopSub=viewPodTopFrame.miniFrame
viewPodTopNameVar=StringVar()
titleLabel(viewPodTopSub,textvariable=viewPodTopNameVar).pack()

#Main Notebook
viewPodNotebookFrame=mainFrame(viewPodScreen)
viewPodNotebookFrame.pack(expand=True,fill=BOTH)
viewPodNotebook=ttk.Notebook(viewPodNotebookFrame)
viewPodNotebook.pack(expand=True,fill=BOTH)

#Basic info
viewPodBasicSection=passwordDisplayView(viewPodNotebook)

viewAccountTitleSection=hiddenDataSection(viewPodBasicSection,"Title")
viewAccountUsernameSection=hiddenDataSection(viewPodBasicSection,"Username")
viewAccountPasswordSection=hiddenDataSection(viewPodBasicSection,"Password")

viewPodBasicSection.addPasswordSection(viewAccountTitleSection)
viewPodBasicSection.addPasswordSection(viewAccountUsernameSection)
viewPodBasicSection.addPasswordSection(viewAccountPasswordSection)
viewPodBasicSection.showSections()

#Advanced info
viewPodAdvancedSection=displayView(viewPodNotebook)

#Add pages
viewPodNotebook.add(viewPodBasicSection,text="Basic")
viewPodNotebook.add(viewPodAdvancedSection,text="Advanced")

#===============================(FUNCTIONS)===============================

#=========Utility Functions=========

def insertEntry(entry,message):
	entry.delete(0,END)
	entry.insert(END,message)

def askMessage(pre,message):
	try:
		messagebox.showinfo(pre,message)
	except:
		print(message)

#=========Program Functions=========

def lockdown():
	"""
	The lockdown function is used
	to lock the master pod and return
	to the open file screen
	"""
	homePodListbox.fullClear()
	openMasterScreen.show()

def goHome():
	"""
	The go home function returns to the home
	screen depending on what screen is loaded
	"""
	currentScreen=mainScreen.currentScreen
	if currentScreen in lockedScreens:
		openScreen.show()
	else:
		homeScreen.show()

def addPodsToListbox(listbox,pods):
	listbox.fullClear()
	for pod in pods:
		listbox.addItem(pod,pods[pod])

def loadFilesInDirectory():
	"""
	This function will scan the current directory
	of the python program to locate any pod files
	"""
	filesFound=[]
	#Traverse current folder
	for root, dirs, files in os.walk(currentDirectory, topdown=False):
		for name in files:
			if name.endswith(".mp"):
				filesFound.append(name)

	#Create Master Pods and display them
	for item in filesFound:
		pod=masterPod(item)
		#Adds to listbox and removes extension
		openMainListbox.addItem(os.path.splitext(item)[0],pod)

def openMasterPod():
	"""
	This function is for when the user
	attempts to open a master pod file
	"""
	current=openMainListbox.getSelected()
	if current != None:
		#Load screen to enter master password
		openMasterScreen.show()
		openMasterTopVar.set(current.getRootName())
		#Load master pod
		masterPod.currentLoadedPod=current

	else:
		askMessage("Select","No Pod Selected")

def unlockMasterPod():

	attempt=openMasterEntry.get()
	if len(attempt.split()) > 0:
		currentMasterPod=masterPod.currentLoadedPod

		#Attempt to unlock
		response=currentMasterPod.unlock(attempt)
		if response != None and response != False:
			print("Unlock success")
			#Track the pods found
			podDict={}
			for item in response:
				#Create pod instance
				pod=dataPod(item,currentMasterPod)
				podDict[item]=pod

				#Add the pod data
				podData=response[item]
				print(podData)
				for item in podData:
					pod.addData(item,podData[item])
			#Load screen
			homeScreen.show()
			#Show Pods
			addPodsToListbox(homePodListbox,podDict)
		else:
			askMessage("Incorrect","Password Incorrect")
	else:
		askMessage("Blank","Please Enter Something")

	#Clear entry
	insertEntry(openMasterEntry,"")

def openDataPod():
	"""
	This function opens
	a normal data pod
	"""
	selectedPod=homePodListbox.getSelected()
	if selectedPod != None and selectedPod != False:
		#Show screen
		viewPodScreen.show()
		#Set label
		viewPodTopNameVar.set(selectedPod.podName)
		#Add data to screen
		addPodDataToScreen(selectedPod,viewPodBasicSection)

def addPodDataToScreen(podInstance,displayViewInstance):
	if type(displayViewInstance) == passwordDisplayView:
		podVault=podInstance.getVault()
		podTitle=podInstance.podName
		if "Title" not in podVault:
			insertEntry(displayViewInstance.sectionDict["Title"],podTitle)
		else:
			print("Its fine")
		for item in podVault:
			if item in displayViewInstance.sectionDict:
				entryToAdd=displayViewInstance.sectionDict[item]
				insertEntry(entryToAdd,podVault[item])



#===============================(BUTTONS)===============================

#=====OPEN SCREEN=====
openSelectFileButton.config(command=openMasterPod)
#=====MASTER SCREEN=====
openMasterUnlockButton.config(command=unlockMasterPod)
openMasterCancelButton.config(command=lambda: openScreen.show())
#===============================(BINDINGS)===============================

#=====STATUS BAR=====
statusBar.addBinding("<Double-Button-1>",lambda event: goHome())
#=====OPEN SCREEN=====
openMainListbox.bind("<Double-Button-1>", lambda event: openMasterPod())
openMainListbox.bind("<Return>", lambda event: openMasterPod())
#=====MASTER SCREEN=====
openMasterEntry.bind("<Return>", lambda event: unlockMasterPod())
#=====VIEW POD SCREEN=====
homePodListbox.bind("<Double-Button-1>", lambda event: openDataPod())

#===============================(MENU CASCADES)===============================
mainMenu.add_cascade(label="File",menu=fileMenu)
mainMenu.add_cascade(label="Edit",menu=editMenu)
mainMenu.add_cascade(label="View",menu=viewMenu)

#==File==
fileMenu.add_command(label="Lockdown",command=lockdown)
#===============================(INITIALISER)===============================
loadFilesInDirectory()
#===============================(TESTING AREA)===============================

#===============================(END)===============================
window.mainloop()