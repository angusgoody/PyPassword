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
openTopFrame=mainFrame(openScreen)
openTopFrame.pack(side=TOP,fill=X)

mainLabel(openTopFrame,text="Select Pod Or Create New One",font="Helvetica 17").pack(expand=True)

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

#===============================(FUNCTIONS)===============================

#=========Utility Functions=========

def insertEntry(entry,message):
	entry.delete(0,END)
	entry.insert(END,message)

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




#===============================(INITIALISER)===============================
loadFilesInDirectory()
#===============================(TESTING AREA)===============================

#===============================(END)===============================
window.mainloop()