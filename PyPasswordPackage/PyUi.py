# coding=utf-8


#Angus Goody
#PyPassword 2.0
#02/06/17

#Main User Interface Module


"""
This file is a custom user interface module
that uses tkinter. It is used so all the
user interface code does not take up the
main __init__ file.
"""

#==================================(IMPORTS)=============================
from tkinter import *
from tkinter import ttk
#==================================(FUNCTIONS)=============================

#==================================(CLASSES)=============================


#==============Master Classes==============

class advancedListbox(Listbox):
	"""
	The advanced Listbox is based on
	the listbox class and adds more functionality
	and makes it easier to track elements
	"""
	def __init__(self,parent,**kwargs):
		Listbox.__init__(self,parent,**kwargs)

		#Track data in listbox
		self.listData={}

		#Add a scrollbar
		self.scrollbar=Scrollbar(self)
		self.scrollbar.pack(side=RIGHT,fill=Y)

		self.scrollbar.config(command=self.yview)
		self.config(yscrollcommand=self.scrollbar.set)


	def addItem(self,textToDisplay,objectInstance):
		"""
		The add function allows an object
		to be added to the listbox and display plain
		text
		"""
		self.listData[textToDisplay]=objectInstance
		self.insert(END,textToDisplay)

	def getSelected(self):
		"""
		This method will attempt to return
		the selected object
		"""
		index=0
		try:
			index =self.curselection()
		except:
			print("Method called on static listbox")
		else:
			try:
				value=self.get(index)
			except:
				pass
			else:
				for item in self.listData:
					if item == value:
						return self.listData[item]

	def fullClear(self):
		"""
		The clear method will delete
		everything in the listbox and remove
		from dictionary as well
		"""
		self.delete(0,END)
		self.listData.clear()

class mainButton(Button):
	"""
	The main button class is mainly
	used to track all the buttons
	on the screen but can be used
	to modify styles of the button
	"""
	def __init__(self,parent,*args,**kwargs):
		Button.__init__(self,parent,kwargs)

class mainFrame(Frame):
	"""
	The Main Frame class is a modified tkinter Frame
	that adds more customization and flexibility, for
	example changing colour and bindings etc.
	"""
	def __init__(self,parent,**kwargs):
		Frame.__init__(self,parent,kwargs)

	def addBinding(self,bindButton,bindFunction):
		"""
		This method will allow the widget
		to be binded with a better binding function
		"""
		self.bind(bindButton,bindFunction)

class mainLabel(Label):
	"""
	The mainLabel class is similar to the mainFrame
	in the fact it is based off an existing tkinter
	widget. It adds more options to the Label widget
	which makes it easier to change colours and fonts
	and also hover bindings etc.
	"""
	def __init__(self,parent,**kwargs):
		Label.__init__(self,parent,kwargs)

class titleLabel(mainLabel):
	"""
	The title label is a class
	for displaying labels that
	are important
	"""
	def __init__(self,parent,**kwargs):
		mainLabel.__init__(self,parent,**kwargs)
		self.config(font="Helvetica 17")

class mainScreen(mainFrame):
	"""
	The mainScreen class is a class
	for each screen of a program. It takes
	care of loading screens and hiding others
	and can execute commands when loaded etc
	"""
	screens=[]
	lastScreen=None
	currentScreen=None

	def __init__(self,parent,screenName,statusVar,**kwargs):
		mainFrame.__init__(self,parent)
		self.screenName=screenName
		self.statusVar=statusVar
		self.parent=parent

		#Add screen to list of screens
		mainScreen.screens.append(self)

		#Get menu to use with screen
		self.mainMenu=kwargs.get("menu")

	def show(self):
		"""
		The show method that will display
		the screen on the screen and update
		the statusVar to the name of the screen
		"""
		if self != mainScreen.lastScreen:
			for screen in mainScreen.screens:
				screen.pack_forget()
			self.pack(expand=True,fill=BOTH)

			#Update statusVar
			self.statusVar.set(self.screenName)
			#Update last screen
			mainScreen.lastScreen=self
			mainScreen.currenScreen=self
			#Update menu
			if self.mainMenu != None:
				self.parent.config(menu=self.mainMenu)

class displayView(mainFrame):
	"""
	This display View class is a class
	that allows multiple frames
	to be shown together in a nice
	format. It evenly spreads each frame
	out and takes care of colouring etc
	"""

	def __init__(self,parent):
		mainFrame.__init__(self,parent)
		self.sections=[]

	def addSection(self,frameToShow):
		self.sections.append(frameToShow)

	def showSections(self):
		for item in self.sections:
			item.pack(expand=True,fill=BOTH)

class topStrip(mainFrame):
	"""
	The stopStrip class is a class
	that is used to go at the top of
	a screen to display information
	"""
	def __init__(self,parent,textVar):
		mainFrame.__init__(self,parent)
		self.textVar=textVar

		#Label
		self.labelView=titleLabel(self,textvariable=self.textVar)
		self.labelView.pack(expand=True)

class centerFrame(mainFrame):
	def __init__(self,parent):
		mainFrame.__init__(self,parent)

		self.miniFrame=mainFrame(self)
		self.miniFrame.pack(expand=True)

class hiddenDataSection(mainFrame):
	"""
	This class is used to display sensitive
	information such as password or username
	"""
	def __init__(self,parent,title):
		mainFrame.__init__(self,parent)
		self.title=title
		self.data=StringVar()
		self.centerFrame=mainFrame(self)
		self.centerFrame.pack(expand=True)

		self.titleLabel=mainLabel(self.centerFrame,text=self.title+":",width=10)
		self.titleLabel.grid(row=0,column=0)

		self.dataEntry=Entry(self.centerFrame)
		self.dataEntry.grid(row=0,column=1)

		self.hideButton=Button(self.centerFrame,text="Hide",command=self.toggleHide,width=6)
		self.hideButton.grid(row=0,column=2,padx=5)

		self.hiddenVar=False

	def addData(self,dataToAdd):
		self.dataEntry.delete(0,END)
		self.dataEntry.insert(END,dataToAdd)

	def toggleHide(self):
		"""
		This method is used to toggle
		whether the data in the entry
		is hidden or revealed
		"""
		if self.hiddenVar == False:
			self.dataEntry.config(show="•")
			self.hideButton.config(text="Show")
			self.hiddenVar=True
		else:
			self.dataEntry.config(show="")
			self.hideButton.config(text="Hide")
			self.hiddenVar=False



