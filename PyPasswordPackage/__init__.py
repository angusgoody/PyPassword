# coding=utf-8


#Angus Goody
#PyPassword 2.0
#02/06/17

#Main Init File

#===============================(IMPORTS)===============================
from tkinter import *
from tkinter import messagebox
import random

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

#===============================(USER INTERFACE)===============================

#-----Open Screen----
openScreen=mainScreen(window,"PyPassword",statusVar)
openScreen.show()

#--Top--
openTopFrame=mainFrame(openScreen)
openTopFrame.pack(side=TOP,fill=X)

mainLabel(openTopFrame,text="Select Pod Or Create New One").pack(expand=True)

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

openCreateFileButton=mainButton(openBottomButtonFrame,text="Create Pod")
openCreateFileButton.pack(side=LEFT)
openSelectFileButton=mainButton(openBottomButtonFrame,text="Open Selected")
openSelectFileButton.pack(side=RIGHT)
#============Choose File screen===========
chooseFileScreen=mainScreen(window,"Choose file",statusVar,menu=lockScreenMenu)
#===============================(END)===============================
window.mainloop()