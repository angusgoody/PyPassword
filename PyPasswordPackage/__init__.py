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

#===============================(USER INTERFACE)===============================

#-----Open Screen----
# region open screen
openScreen=mainScreen(window,"PyPassword",statusVar,menu=lockScreenMenu)
openScreen.show()

#--Top--
openTopVar=StringVar()
openTopVar.set("Select Pod Or Create New One")
openTopFrame=topStrip(openScreen,openTopVar)
openTopFrame.pack(side=TOP,fill=X)

#--Main--
openMainFrame=mainFrame(openScreen)
openMainFrame.pack(expand=True,fill=BOTH)

openMainListbox=advancedListbox(openMainFrame)
openMainListbox.pack(expand=True,fill=BOTH)

#--Bottom--
openBottomFrame=mainFrame(openScreen)
openBottomFrame.pack(fill=X,side=BOTTOM)

openBottomButtonFrame=mainFrame(openBottomFrame)
openBottomButtonFrame.pack(expand=True)

openCreateFileButton=mainButton(openBottomButtonFrame,text="Create Pod",width=12)
openCreateFileButton.pack(side=LEFT,padx=5)
openSelectFileButton=mainButton(openBottomButtonFrame,text="Open Selected",width=12)
openSelectFileButton.pack(side=RIGHT,padx=5)

#endregion

#----Open Master Password Screen-----
#region master screen
openMasterScreen=mainScreen(window, "Master Password", statusVar)

openMasterDisplay=displayView(openMasterScreen)
openMasterDisplay.pack(expand=True,fill=BOTH)

#--Top Section--
openMasterTopFrame=mainFrame(openMasterDisplay)
openMasterSub=mainFrame(openMasterTopFrame)
openMasterSub.pack(expand=True)

mainLabel(openMasterSub,text="File: ",font="Helvetica 17").pack(side=LEFT)
openMasterTopVar=StringVar()
openMasterTopVar.set("None")
mainLabel(openMasterSub,textvariable=openMasterTopVar,font="Helvetica 17").pack(side=RIGHT)

#--Main Section--
openMasterMainFrame=mainFrame(openMasterDisplay)
openMasterSub=mainFrame(openMasterMainFrame)
openMasterSub.pack(expand=True)

mainLabel(openMasterSub,text="Enter password").pack()
openMasterEntry=Entry(openMasterSub,show="•")
openMasterEntry.pack()

#--Bottom Section--
openMasterBottomFrame=mainFrame(openMasterDisplay)
openMasterBottomSub=mainFrame(openMasterBottomFrame)
openMasterBottomSub.pack(expand=True)

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

def openSelected():
	"""
	This function is for when the user
	attempts to open a master pod file
	"""
	current=openMainListbox.getSelected()
	if current != None:
		#Load screen to enter master password
		openMasterScreen.show()
		openMasterTopVar.set(current.getRootName())

	else:
		askMessage("Select","No Pod Selected")




#===============================(BUTTONS)===============================

#=====OPEN SCREEN=====
openSelectFileButton.config(command=openSelected)
#===============================(BINDINGS)===============================
openMainListbox.bind("<Double-Button-1>",lambda event: openSelected())

#===============================(INITIALISER)===============================
loadFilesInDirectory()
#===============================(TESTING AREA)===============================

#===============================(END)===============================
window.mainloop()