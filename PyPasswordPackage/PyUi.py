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
import random
import datetime

#==============LOG CLASS==============

class logClass():
	"""
	The log class will store a log
	for everything and record
	errors etc
	"""
	allLogs={}
	def __init__(self,logName):
		self.logName=logName
		#Where the data is stored
		self.dataDict={}
		self.systemDict={}
		#Add the log to log dict
		logClass.allLogs[self.logName]=self

	def report(self,message,variable,*extra,**kwargs):

		"""
		The report method is the main
		method that is called to report
		something to the log and the current
		time is recorded and tags can be used
		to group errors
		"""
		#Gether message
		message=message+" "
		message+=variable
		if len(extra) > 0:
			for item in extra:
				message+=" "
				message+=item
		#Gather Tag
		tag="Default"
		if "tag" in kwargs:
			tag=kwargs["tag"]

		#Get time
		currentTime=datetime.datetime.now().time()

		defaultDict=self.dataDict
		#Check if system or not
		if "system" in kwargs:
			if kwargs["system"]:
				defaultDict=self.systemDict

		#Create dictionary and add data
		if tag not in defaultDict:
			defaultDict[tag]=[]
		defaultDict[tag].append({"Time":currentTime,"Tag":tag,"Message":message})

log=logClass("User Interface")


#==================================(FUNCTIONS)=============================

#==============HEX FUNCTIONS================

def convertHex(value,intoDecOrHex):
	"""
	Convert a decimal to hex or hex to decimal
	"""
	if intoDecOrHex == "Decimal":
		return int("0x" + str(value), 16)
	else:
		hexValue = "#"
		hexValue = hexValue + str((format(value, '02x')).upper())
		return hexValue

def getHexSections(hexValue):
	"""
	This will split a 6 digit hex number into pairs and store them
	in an array
	"""
	if len(hexValue) <= 7 and "#" in hexValue:
		#Removes the #
		colourData = hexValue.replace("#", "")
		# Split HEX number into pairs
		colourSections = [colourData[i:i + 2] for i in range(0, len(colourData), 2)]
		return colourSections

def getDecimalHexSections(hexValue):
	hexSections=getHexSections(hexValue)
	decimalArray=[]
	for item in hexSections:
		decimalValue=convertHex(item,"Decimal")
		decimalArray.append(decimalValue)
	return decimalArray

def getColourForBackground(hexValue):
	"""
	This function will return white or black as a text colour
	depending on what the background colour passed to it is. For
	example if a dark background is passed then white will be returned because
	white shows up on dark best.
	"""
	chosenColour="Black"
	whiteCounter = 0

	#Checks the hex number is standard
	if len(hexValue) <= 7 and "#" in hexValue:

		colourSections=getHexSections(hexValue)
		for x in colourSections:
			#Convert to decimal
			y=convertHex(x,"Decimal")
			#If its less than half way between 0 and FF which is 255
			if y < 128:
				whiteCounter += 1
		if whiteCounter > 1:
			#White is returned
			chosenColour = "#ffffff"
		else:
			#Black is returned
			chosenColour = "#000000"
	return chosenColour

def generateHexColour():
	"""
	This function will generate a random HEX colour

	"""
	baseNumber=random.randint(1,16777216)
	hexValue=convertHex(baseNumber,"Hex")
	hexLeng=len(hexValue)
	while hexLeng != 7:
		hexValue=hexValue+"0"
		hexLeng=len(hexValue)
	return hexValue

#==============OTHER FUNCTIONS================

def insertEntry(entry,message):
	entry.delete(0,END)
	entry.insert(END,message)

def insertDisabledEntry(entry,message):
	entry.config(state=NORMAL)
	insertEntry(entry,message)
	entry.config(state=DISABLED)

def recursiveChangeColour(parent,colour,fgColour):
	"""
	This function will recursivly search all children
	of an element and change their colour
	"""
	widgetArray =["Entry", "Button", "Text", "Listbox", "OptionMenu", "Menu"]
	parentClass=parent.winfo_class()
	if parentClass == "Frame":
		parent.config(bg=colour)
		children=parent.winfo_children()
		for item in children:
			recursiveChangeColour(item,colour,fgColour)
	else:
		try:
			#Certain widgets need diffrent attention
			if parent.winfo_class() in widgetArray:
					parent.config(highlightbackground=colour)
			else:
				parent.config(bg=colour)

			#Update labels so they show up on certain colours
			if parent.winfo_class() == "Label":
					parent.changeColour(getColourForBackground(colour))

		except:
			pass

def recursiveBind(parent,bindButton,bindFunction):
	"""
	This function is very important because python
	only binds functions to one item. This function will
	bind all the children of that item to the same function.
	"""
	parentClass=parent.winfo_class()
	if parentClass == "Frame":
		parent.bind(bindButton,bindFunction)
		children=parent.winfo_children()
		for item in children:
			recursiveBind(item,bindButton,bindFunction)
	else:
		try:
			parent.bind(bindButton,bindFunction)
		except:
			pass
	log.report("Added recursive binding to",parent.winfo_class(),tag="binding",system=True)
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

	def addItem(self,textToDisplay,objectInstance,**kwargs):
		"""
		The add function allows an object
		to be added to the listbox and display plain
		text
		"""
		self.listData[textToDisplay]=objectInstance
		self.insert(END,textToDisplay)

		#Change colour
		colour=generateHexColour()
		if "colour" in kwargs:
			colour=kwargs["colour"]
		self.itemconfig(END,bg=colour)

		#Change FG
		try:
			fgColour=getColourForBackground(colour)
		except:
			log.report("Error getting fg colour for",colour,tag="Error",system=True)
		else:
			self.itemconfig(END,fg=fgColour)
	def getSelected(self):
		"""
		This method will attempt to return
		the selected object
		"""
		index=0
		try:
			index =self.curselection()
		except:
			log.report("Method called on static listbox", "(Get Selected)", tag="error", system=True)
		else:
			try:
				value=self.get(index)
			except:
				log.report("Error getting value from listbox", "(Get Selected)", tag="error", system=True)
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
		log.report("Listbox has been cleared of data", "(FullClear)", system=True)

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
		Frame.__init__(self,parent)
		if "colour" in kwargs:
			self.colour(kwargs["colour"])
		self.colourVar=None

	def addBinding(self,bindButton,bindFunction):
		"""
		This method will allow the widget
		to be binded with a better binding function
		"""
		recursiveBind(self,bindButton,bindFunction)



	def colour(self,chosenColour):
		"""
		The colour method will update
		the colour of the frame
		and all its children
		"""
		#Get FG colour for selected colour
		fgColour=getColourForBackground(chosenColour)
		self.colourVar=chosenColour

		#Recursivley search through all children and change colour
		recursiveChangeColour(self,chosenColour,fgColour)

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

	def changeColour(self,colour):
		self.config(fg=colour)

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
			mainScreen.currentScreen=self
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

class passwordDisplayView(displayView):
	"""
	This class is a modified display view
	that holds passwords and usernames etc
	"""
	def __init__(self,parent):
		displayView.__init__(self,parent)
		self.sectionDict={}

	def addPasswordSection(self,hiddenDataSection):
		"""
		Overides the default add section method
		because title needs to be stored in the
		object
		"""
		self.addSection(hiddenDataSection)
		self.sectionDict[hiddenDataSection.title]=hiddenDataSection

	def disable(self):
		"""
		The disable method will make the view "Read only"
		and make it not possible to edit the data
		:return:
		"""
		pass

	def createSections(self,titleList,colourList):
		"""
		This method bulk creates sections in the displayView
		"""
		if len(titleList) == len(colourList):
			for title in titleList:
				newSection=hiddenDataSection(self,title)
				newSection.colour(colourList[titleList.index(title)])
				self.addPasswordSection(newSection)

	def clearScreem(self):
		"""
		This method will wipe all data from the
		screen and dictionary
		"""
		for item in self.sectionDict:
			self.sectionDict[item].clear()

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
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

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

		self.dataEntry=Entry(self.centerFrame,state=DISABLED)
		self.dataEntry.grid(row=0,column=1)

		self.hideButton=Button(self.centerFrame,text="Hide",command=self.toggleHide,width=6)
		self.hideButton.grid(row=0,column=2,padx=5)

		#Edit variables
		self.hiddenVar=False
		self.editMode=False

	def addData(self,dataToAdd):
		"""
		This method will add data to the section
		by inserting the data into the entry and
		updting the string variable
		"""
		self.dataEntry.config(state=NORMAL)
		insertEntry(self.dataEntry,dataToAdd)
		self.data.set(dataToAdd)
		if self.editMode == False:
			self.dataEntry.config(state=DISABLED)

	def toggleHide(self):
		"""
		This method is used to toggle
		whether the data in the entry
		is hidden or revealed
		"""
		if self.hiddenVar == False:
			self.dataEntry.config(show="•")
			self.hideButton.config(text="Show")
			self.dataEntry.config(state=DISABLED)
			self.hiddenVar=True
		else:
			self.dataEntry.config(show="")
			self.hideButton.config(text="Hide")
			self.hiddenVar=False
			if self.editMode == False:
				self.dataEntry.config(state=DISABLED)
			else:
				self.dataEntry.config(state=NORMAL)

	def restoreData(self):
		"""
		This method will restore the original
		data to the entry if it is edited by
		user
		"""
		self.addData(self.data.get())

	def clear(self):
		"""
		Remove data from entry and
		the string var
		"""
		insertEntry(self.dataEntry,"")
		self.data.set("")

	def enableEditing(self):
		"""
		This method allows the section to be edited
		and changed
		"""
		self.editMode=True
		self.dataEntry.config(state=NORMAL)

	def disableEditing(self):
		"""
		This method disables the section and returns
		to read only
		"""
		self.editMode=False
		self.dataEntry.config(state=DISABLED)

	def getData(self):
		return self.dataEntry.get()

	def updateData(self):
		"""
		This method will get the data
		from the entry and then update the data
		"""
		newData=self.dataEntry.get()
		self.data.set(newData)

class multiView(mainFrame):
	"""
	The multiview class is a class that allows
	multiple frames to be viewed in the same place
	by changing frames with simple methods
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

		#Stores the views
		self.views=[]

		self.lastView=None
		self.currentView=None

	def addView(self,frameToShow):
		#Add a certain frame to the dictionary
		if frameToShow not in self.views:
			self.views.append(frameToShow)

	def showView(self,frameToShow):
		"""
		The show view method when called will show
		a certain frame in the dictionary. This value
		is referenced using an indicator string
		"""
		if frameToShow in self.views:
			if frameToShow != self.lastView:
				for item in self.views:
					item.pack_forget()
				frameToShow.pack(expand=True,fill=BOTH)
		else:
			log.report("Non registered frame attempted to be show",frameToShow,tag="Error",system=True)



