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

openDisplay=displayView(openScreen)
openDisplay.pack(expand=True,fill=BOTH)

#Existing files
openExistingFrame=mainFrame(openDisplay)
openExistingButton=mainButton(openExistingFrame,text="Open Master Pod",width=15)
openExistingButton.pack(expand=True)

#Create new files
openNewFrame=mainFrame(openDisplay)
openNewButton=mainButton(openNewFrame,text="Create New Master Pod",width=15)
openNewButton.pack(expand=True)

#Add Views
openDisplay.addSection(openExistingFrame)
openDisplay.addSection(openNewFrame)
openDisplay.showSections()

#============Choose File screen===========
chooseFileScreen=mainScreen(window,"Choose file",statusVar,menu=lockScreenMenu)
#===============================(END)===============================
window.mainloop()