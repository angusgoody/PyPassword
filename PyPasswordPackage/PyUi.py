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

#Stores the main TK windos for __init__ to use in this program
mainWindow=None

def getData(dataSource):
	"""
	This function will get data from a number
	of different widgets
	"""
	valids=[Entry,Text]
	if type(dataSource) == Entry:
		return dataSource.get()
	elif type(dataSource) == Text:
		return dataSource.get("1.0",END)
	else:
		log.report("Not able to get data from",dataSource)

def addUIWindow(window):
	global mainWindow
	"""
	Allows a tk window to be added
	to this program
	"""
	mainWindow=window

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
		#Store the tree view the data is stored in
		self.defaultTree=None
		self.systemTree=None

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
		system=False
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
				system=True

		#Create dictionary and add data
		if tag not in defaultDict:
			defaultDict[tag]=[]
		defaultDict[tag].append({"Time":currentTime,"Tag":tag,"Message":message})

		#Add to listbox if there is one

		if system:
			self.addDataToTree(message,currentTime,True)
		else:
			self.addDataToTree(message,currentTime,False)

	def addTree(self,indicator,tree):
		"""
		Assign a tree to export to for
		each option. System info and default info
		"""
		if indicator == "System":
			self.systemTree=tree
		elif indicator == "Default":
			self.defaultTree=tree


	def addDataToTree(self,data,time,system):
		"""
		This method will take the time and data
		provided and insert it into the tree
		"""
		if system:
			#Add to system tree
				if self.systemTree != None:
					self.systemTree.insert("" , 0,values=(data,time))
		else:
			if self.defaultTree != None:
				self.defaultTree.insert("" , 0,values=(data,time))

log=logClass("UI")


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
	if type(entry) == Entry:
		entry.delete(0,END)
		entry.insert(END,message)
	elif type(entry) == Text:
		entry.delete("1.0",END)
		entry.insert("1.0",message)



def recursiveChangeColour(parent,colour,fgColour):
	"""
	This function will recursivly search all children
	of an element and change their colour
	"""
	widgetArray =["Entry", "Button", "Text", "Listbox", "OptionMenu", "Menu"]
	excludeArray=[advancedNotebook]
	parentClass=parent.winfo_class()
	if type(parent) not in excludeArray:
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

def deleteItemFromListbox(listbox,indicator):
	counter=-1
	for item in listbox.get(0,END):
		counter+=1
		if item == indicator:
			listbox.delete(counter,counter)
			break

#==================================(CLASSES)=============================


#==============Master Classes==============

class mainButton(Button):
	"""
	The main button class is mainly
	used to track all the buttons
	on the screen but can be used
	to modify styles of the button
	"""
	def __init__(self,parent,*args,**kwargs):
		Button.__init__(self,parent,kwargs)
		self.config(relief=FLAT)

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

	def addPodList(self,poDict):
		"""
		This method can add a dictionary of data
		pods to the listbox
		"""
		self.fullClear()
		for item in poDict:
			self.addItem(item,poDict[item])

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

	def removeItem(self,indicator,tempOrNot):
		"""
		This method will remove an item
		from the listbox. The indicator is used
		to identify the item to remove and tempOrNot 
		determines the refrence from the dict or not.
		"""
		if indicator in self.listData:
			deleteItemFromListbox(self,indicator)
			#if not temp it removes reference from dict
			if tempOrNot == False:
				del self.listData[indicator]
			log.report("Removed item from listbox",indicator)
		else:
			log.report("Unable to remove item from listbox not in dict",indicator)
			print("Unable")

	def updateItemLabel(self,oldName,newName):
		for item in self.listData:
			if item == oldName:
				listData=self.listData[oldName]
				self.removeItem(oldName,True)
				self.addItem(newName,listData)
				break

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

			if mainScreen.lastScreen != None:
				mainScreen.lastScreen.pack_forget()
			self.pack(expand=True,fill=BOTH)

			#Update statusVar
			self.statusVar.set(self.screenName)
			#Update last screen
			mainScreen.lastScreen=self
			mainScreen.currentScreen=self
			#Update menu
			if self.mainMenu != None:
				self.parent.config(menu=self.mainMenu)
			#Report to log
			log.report("Showing screen",self.screenName,tag="Screen")

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

	def addSection(self,frameToShow,**kwargs):
		self.sections.append(frameToShow)
		if "colour" in kwargs:
			frameToShow.colour(kwargs["colour"])

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
		#The section dict stores hiddenData sections with key of name
		self.sectionDict={}

	def addPasswordSection(self,hiddenDataSection,**kwargs):
		"""
		Overides the default add section method
		because title needs to be stored in the
		object
		"""
		self.addSection(hiddenDataSection,**kwargs)
		self.sectionDict[hiddenDataSection.title]=hiddenDataSection

	def createSections(self,titleList,colourList):
		"""
		This method bulk creates sections in the displayView
		"""
		for title in titleList:
			newSection=hiddenDataSection(self,title)
			try:
				newSection.colour(colourList[titleList.index(title)])
			except:
				pass
			self.addPasswordSection(newSection)

	def clearScreen(self):
		"""
		This method will wipe all data from the
		screen and dictionary
		"""
		for item in self.sectionDict:
			#Remove refrence
			self.sectionDict[item].clear()

	def addCustomScreen(self,frameToShow,dataSource,title):
		"""
		The add custom screen allows a custom frame
		to be added to the password display view
		"""
		self.addSection(frameToShow)

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
	"""
	A center frame is a frame that
	automatically creates a sub frame
	that will be in the center of the
	screen
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

		self.miniFrame=mainFrame(self)
		self.miniFrame.pack(expand=True)

class dataSection(centerFrame):
	"""
	This class is a mainFrame that wil be able
	to store data and display a title. It will
	be used for custom password sections that require
	more than the standard hidden data section.
	"""
	def __init__(self,parent,title,**kwargs):
		centerFrame.__init__(self,parent,**kwargs)

		self.title=title
		self.dataSource=None

		#Key variables
		self.editData=False
		self.data=StringVar()


	def addDataSource(self,dataSource):
		self.dataSource=dataSource

	def getData(self):
		"""
		This method will get data for a number
		of diffrent widgets and return the data
		"""
		if self.dataSource != None:
			return getData(self.dataSource)

	def insertData(self,dataToAdd):
		"""
		The method that adds data to the range
		of data sources that this class will have
		"""
		if self.dataSource != None:
			self.enableDataSource()
			insertEntry(self.dataSource,dataToAdd)
			if self.editData == False:
				self.disableDataSource()

	def clear(self):
		"""
		This method removes all data from the object
		so it can be used by another pod
		"""
		if self.dataSource != None:
			self.insertData("")
		self.data.set("")

	def disableDataSource(self):
		"""
		This method will disable the objects data source
		so the user is unable to edit it
		"""
		self.editMode=False
		if self.dataSource != None:
			self.dataSource.config(state=DISABLED)
			#Text boxes are hard to tell if disabled or not
			if type(self.dataSource) == Text:
				self.dataSource.config(fg="#919591")

	def enableDataSource(self):
		"""
		This method will make the data source
		available to edit again
		"""
		self.editMode=True
		if self.dataSource != None:
			self.dataSource.config(state=NORMAL)
			#Text boxes are hard to tell if disabled or not
			if type(self.dataSource) == Text:
				self.dataSource.config(fg="#000000")

	def addData(self,dataToAdd):
		"""
		This method will add data to the section
		by inserting the data into the entry and
		updting the string variable
		"""
		if self.dataSource != None:
			self.enableDataSource()
			self.insertData(dataToAdd)
			self.data.set(dataToAdd)
			if self.editMode == False:
				self.dataSource.config(state=DISABLED)

	def restoreData(self):
		"""
		This method will restore the original
		data to the entry if it is edited by
		user
		"""
		self.addData(self.data.get())

	def updateData(self):
		"""
		This method will get the data
		from the entry and then update the data
		"""
		if self.dataSource != None:
			newData=self.getData()
			self.data.set(newData)

class hiddenDataSection(dataSection):
	"""
	This class is used to display sensitive
	information such as password or username
	"""
	def __init__(self,parent,title):
		dataSection.__init__(self,parent,title)

		self.title=title
		self.data=StringVar()

		self.centerFrame=self.miniFrame

		self.titleLabel=mainLabel(self.centerFrame,text=self.title+":",width=10)
		self.titleLabel.grid(row=0,column=0)

		self.dataEntry=Entry(self.centerFrame,state=DISABLED)
		self.dataEntry.grid(row=0,column=1)
		self.addDataSource(self.dataEntry)

		self.buttonFrame=mainFrame(self.centerFrame)
		self.buttonFrame.grid(row=0,column=2,padx=7)

		#Edit variables
		self.hiddenVar=False
		self.editMode=False

		#Store Buttons
		self.buttonDict={}
		self.buttonCounter=0

		#Create preset buttons (Array used because order matters)
		initButtons=[["Hide",lambda s=self:s.toggleHide()],["Copy",lambda s=self: s.copyData()]]
		for but in initButtons:
			self.addButton(but[0])
			self.addButtonCommand(but[0],but[1])

	def toggleHide(self):
		"""
		This method is used to toggle
		whether the data in the entry
		is hidden or revealed
		"""
		if self.hiddenVar == False:
			self.dataEntry.config(show="•")
			self.buttonDict["Hide"].config(text="Show")
			self.disableDataSource()
			self.hiddenVar=True
		else:
			self.dataEntry.config(show="")
			self.buttonDict["Hide"].config(text="Hide")
			self.hiddenVar=False
			if self.editMode == False:
				self.disableDataSource()
			else:
				self.enableDataSource()

	def addButton(self,buttonText):
		"""
		This method will add a button
		to the frame and commands can be
		added later
		"""

		#Create button
		newButton=mainButton(self.buttonFrame,text=buttonText,width=7)
		newButton.grid(row=0,column=self.buttonCounter)
		self.buttonCounter+=1

		#Add to list
		self.buttonDict[buttonText]=newButton

		#Return button
		return newButton

	def addButtonCommand(self,buttonName,command):
		"""
		This method will add a command to one of the buttons
		in the data section
		"""
		if buttonName in self.buttonDict:
			self.buttonDict[buttonName].config(command=command)

	def copyData(self):
		"""
		This method will copy the saved data to the
		clipboard
		"""
		if mainWindow != None:
			mainWindow.clipboard_clear()
			mainWindow.clipboard_append(self.data.get())
			log.report("Added data to clipboard","(Hidden data entry)")

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

class popUpWindow(Toplevel):
	"""
	The popUpWindow Class is a class that
	will display a pop up window to the user
	and disable the main window.
	"""
	def __init__(self,root,name,**extra):
		Toplevel.__init__(self,root)
		self.name=name
		self.frameToShow=None
		self.root=root
		self.infoStringVar=StringVar()

		if "infoVar" in extra:
			self.infoStringVar=extra["infoVar"]

		#Setup
		self.title(self.name)
		self.geometry("200x200")

		#Initiate any entrys the window will have that needs to store data
		self.entryList=[]
		self.runCommandDict={}
		self.gatheredData=[]

		#Add Buttons to bottom of screen
		self.buttonStrip=centerFrame(self)
		self.buttonStrip.pack(side=BOTTOM,fill=X)
		self.buttonStripSub=self.buttonStrip.miniFrame

		self.cancelButton=mainButton(self.buttonStripSub,text="Cancel",width=8,command=self.cancel)
		self.cancelButton.grid(row=0,column=0)

		self.saveButton=mainButton(self.buttonStripSub,text="Save",width=8,command=self.save)
		self.saveButton.grid(row=0,column=1)

		self.buttonStrip.colour(generateHexColour())

		#Add menu items
		self.menu=Menu(self)
		self.config(menu=self.menu)

		#Variables
		self.saveButtonState=True

	def addView(self,frameToShow):
		self.frameToShow=frameToShow
		frameToShow.pack(expand=True,fill=BOTH)

	def addCommands(self,runCommandList,parameterValue):
		"""
		This method allows a command to be added to the object
		so when the user clicks "Save" a certain command is executed
		the parameterValue determines whether the commands need to
		be given a paramter of the object or not.
		"""
		for item in runCommandList:
			self.runCommandDict[item]=parameterValue

	def run(self):
		self.focus_set()
		self.grab_set()
		self.transient(self.root)

	def cancel(self):
		self.grab_release()
		self.destroy()

	def addDataSource(self,entryList):
		"""
		Allows the user to add refrences to widgets
		that collect data from the user, to it can
		be returned when the "Save" button is run
		"""
		for entry in entryList:
			self.entryList.append(entry)

	def save(self):

		#Gather data
		if len(self.entryList) > 0:
			for item in self.entryList:
				if type(item) == Entry:
					self.gatheredData.append(item.get())
				else:
					log.report("Invalid data source used in popup",item,tag="Error",system=True)
		else:
			log.report("The popup window was not given any data sources and has not returned any data","(UI)",tag="UI")

		#Kill window
		self.cancel()
		#Execute commands
		if len(self.runCommandDict) > 0:
			for command in self.runCommandDict:
				if self.runCommandDict[command]:
					try:
						command(self)
					except:
						log.report("Encountered error when running popup window commands",self.name,tag="Error")
				else:
					try:
						command()
					except:
						log.report("Encountered error when running popup window commands",self.name,tag="Error")

	def toggle(self,state):
		if state == "DISABLED":
			self.saveButton.config(state=DISABLED)
			self.saveButtonState=False
		else:
			self.saveButton.config(state=NORMAL)
			self.saveButtonState=True

#==============TEST==============

class advancedNotebook(mainFrame):
	"""
	The advanced Notebook is
	a custom notebook class that will look
	better and do more than the standard notebook
	class
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)


		#Top view
		self.topBar=centerFrame(self)
		self.topSub=self.topBar.miniFrame
		self.topBar.pack(side=TOP,fill=X)
		self.topBar.colour("#B9BEBD")

		self.views={}
		self.labelDict={}
		self.currentView=None

		self.viewCount=0

		#Colour variables
		self.selectColour="#FFFFFF"
		self.selectFG="#000000"
		self.notSelected="#98A5AA"
		self.notSelectedHover="#AFBCC2"

		#Get a select colour from kwargs
		if "select" in kwargs:
			self.selectColour=kwargs["select"]
			self.selectFG=getColourForBackground(kwargs["select"])
		if "topColour" in kwargs:
			self.topBar.colour(kwargs["topColour"])



	def addView(self,frame,name):
		"""
		This method will add a frame to the notebook
		view and create a label to nagivate with
		"""
		#Add to dictionary
		self.views[name]=frame
		#Add to top bar
		newLabel=mainLabel(self.topSub,text=name,width=10,bg=self.notSelected)
		newLabel.grid(row=0,column=self.viewCount)
		#Add binding
		newLabel.bind("<Button-1>",lambda event, s=self,n=name: s.showView(n))
		newLabel.bind("<Enter>",lambda event,lab=newLabel: lab.config(bg=self.notSelectedHover))
		newLabel.bind("<Leave>",lambda event,lab=newLabel: lab.config(bg=self.notSelected))
		#Add label to dictionary
		self.labelDict[name]=newLabel
		self.viewCount+=1

		#Show view
		if self.viewCount == 1:
			self.showView(name)

	def showView(self,name):
		"""
		This method is run when a screen
		needs to be shown. It will hide and
		show relevant screens and update label
		colours etc.
		"""
		if name in self.views:
			currentViewName=self.currentView
			frameToLoad=self.views[name]

			#Ensure same frame isnt loaded
			if currentViewName != name:
				if currentViewName != None:
					#Hide frame
					self.views[currentViewName].pack_forget()
					#Update label
					self.labelDict[currentViewName].config(bg=self.notSelected)
					#Remove old bindings
					currentLabel=self.labelDict[currentViewName]
					currentLabel.bind("<Enter>",lambda event,lab=currentLabel: lab.config(bg=self.notSelectedHover))
					currentLabel.bind("<Leave>",lambda event,lab=currentLabel: lab.config(bg=self.notSelected))

				#Display the new frame
				frameToLoad.pack(expand=True,fill=BOTH,side=BOTTOM)

				#Update new label
				currentLabel=self.labelDict[name]
				currentLabel.config(bg=self.selectColour)
				currentLabel.config(fg=self.selectFG)
				self.currentView=name
				#Unbind because when selected tab has no bindings
				currentLabel.unbind("<Enter>")
				currentLabel.unbind("<Leave>")


