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
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import os

#Variable for TK windows
mainWindow=None

#==============Styles==============
mainFont="Avenir"

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

	def report(self,message,*extra,**kwargs):

		"""
		The report method is the main
		method that is called to report
		something to the log and the current
		time is recorded and tags can be used
		to group errors
		"""
		#Gether message
		message=message+" "
		system=False
		if len(extra) > 0:
			for item in extra:
				message+=" "
				message+=str(item)
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

import PEM

#==================================(FUNCTIONS)=============================


#=========Utility Functions=========
"""
Utility Functions are handy little
functions that help reduce the amount
of code needed.
"""

def launchWebsite(url):
	"""
	This function will launch the website in the default
	webbrowser
	"""
	if url:
		try:
			if "http://" not in url:
				url="http://"+url
			webbrowser.open_new(url)
		except:
			log.report("Error opening website",url,tag="Error")

def askMessage(pre,message):
	try:
		messagebox.showinfo(pre,message)
	except:
		print(message)

def askFirst(pre,message,command):
	"""
	This little function will
	execute a certain command
	only after the user has clicked 
	"ok"
	"""
	try:
		response=messagebox.askokcancel(pre,message)
	except:
		return False
	else:
		if response:
			command()
		return response

def insertEntry(entry,message):
	"""
	Will insert data into an entry
	and will also work with Text boxes
	"""
	if message == None:
		message=""
	if type(entry) == Entry:
		entry.delete(0,END)
		entry.insert(END,message)

	elif type(entry) == Text:
		entry.delete("1.0",END)
		entry.insert("1.0",message)
	elif type(entry) == labelEntry:
		insertEntry(entry.entry,message)

def getData(dataSource):
	"""
	This function will get data from a number
	of different widgets
	"""
	valids=[Entry,Text]
	if type(dataSource) == Entry:
		return dataSource.get()
	elif type(dataSource) == Text:
		data=dataSource.get("1.0",END)
		if len(data.split()) > 0:
			return data
		else:
			return ""

	#Custom
	elif type(dataSource) == labelEntry:
		return dataSource.entry.get()
	else:
		log.report("Not able to get data from",dataSource)

def addUIWindow(window):
	global mainWindow
	"""
	Allows a tk window to be added
	to this program
	"""
	mainWindow=window

def addDataToClipboard(data):
	if mainWindow != None and data != None:
		if len(data.split()) > 0:
			mainWindow.clipboard_clear()
			mainWindow.clipboard_append(data)
			log.report("Added data to clipboard","(Func)")
		else:
			log.report("No data to copy to clipboard")

def copyDataFromEntry(entry):
	"""
	This function will copy the password generated
	to the clipboard
	"""
	data=getData(entry)
	if data != None:
		addDataToClipboard(data)
		log.report("Added data to clipboard","(Copy)")

	else:
		askMessage("Empty","No data to copy")


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

def recursiveChangeColour(parent,colour,fgColour):
	"""
	This function will recursivly search all children
	of an element and change their colour
	"""
	widgetArray =["Entry", "Button", "Text", "Listbox", "OptionMenu", "Menu"]
	excludeArray=[advancedNotebook, privateNotebook]
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
				if parentClass in widgetArray:
						parent.config(highlightbackground=colour)
				else:

					#Some labels dont need colour updating
					if type(parent) == mainLabel:
						if parent in mainLabel.nonColours:
							print(parent.labelData.get())
						else:
							parent.config(bg=colour)
					else:
						parent.config(bg=colour)

				#Update labels so they show up on certain colours
				if parentClass == "Label":
					parent.changeColour(getColourForBackground(colour))

			except:
				pass
		log.report("Change colour of",type(parent),tag="UI",system=True)

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
	log.report("Added recursive binding to",parent.winfo_class(),tag="UI",system=True)

def deleteItemFromListbox(listbox,indicator):
	counter=-1
	for item in listbox.get(0,END):
		counter+=1
		if item == indicator:
			listbox.delete(counter,counter)
			break

def askForFile():

	try:
		directory=filedialog.askopenfilename(filetypes=(("Master Pod", "*.mp"),
                                           ("All files", "*.*")))
	except:
		log.report("Error launching file dialog","(UI)",tag="Error")

	else:
		if directory != None:
			return directory

def advancedSearch(target, dataToSearch):
	"""
	This function is the actual search
	function and will recursivley search and return
	True or False
	"""
	#Setup
	target=str(target)
	target=target.upper()

	#If string passed to function convert to array
	if type(dataToSearch) == str:
		dataToSearch=[dataToSearch]


	#Iterate through all data
	for item in dataToSearch:

		#If data source is dictionary
		if type(dataToSearch) == dict:
			if advancedSearch(target,dataToSearch[item]):
				return True

		#Get data type
		try:
			dataType=type(item)
		except:
			log.report("Error converting data type to search",tag="error",system=True)
		else:

			#If data is number or float
			if dataType == int or dataType == float:
				item=str(item)
				dataType=type(item)

			#If data is simple string
			if dataType == str:
				if target in item.upper():
					return True
			#If data is list
			elif dataType == list:
				for section in item:
					if advancedSearch(target, [section]):
						return True
			#If data is dictionary
			elif dataType == dict:
				for section in item:
					if advancedSearch(target, section):
						return True
					dataInSection=item[section]
					if advancedSearch(target, [dataInSection]):
						return True
			#If data is a student class
			elif dataType == PEM.dataPod:
				data=item.getInfo()
				if advancedSearch(target, data):
					return True

	return False

def getBaseOfDirectory(value,fileNameOrBaseName):
	"""
	This function will get the base filename
	of a directory stored as a sttring. The fileNameOrBaseName
	variable indicates whether the extension is needed or not.
	file = extension
	else = without extension
	"""
	if fileNameOrBaseName == "file":
		try:
			return os.path.basename(value)
		except:
			return ""
	else:
		try:
			return os.path.splitext(os.path.basename(value))[0]
		except:
			return ""

#==================================(CLASSES)=============================

#==============Classes==============





#==============Master TK Classes==============

class mainButton(Button):
	"""
	The main button class is mainly
	used to track all the buttons
	on the screen but can be used
	to modify styles of the button
	"""
	def __init__(self,parent,*args,**kwargs):
		Button.__init__(self,parent,**kwargs)
		self.config(relief=FLAT)

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
	nonColours=[]
	def __init__(self,parent,**kwargs):

		#Custom kwargs
		hover=False
		if "hover" in kwargs:
			if kwargs["hover"]:
				kwargs.pop("hover")
				hover=True

		if "nonColour" in kwargs:
			if kwargs["nonColour"]:
				mainLabel.nonColours.append(self)
				kwargs.pop("nonColour")
				log.report("Non colour widget added")

		if "font" in kwargs:
			font=kwargs["font"]
			kwargs.pop("font")
		else:
			font=mainFont

		Label.__init__(self,parent,font=font,**kwargs)
		self.labelData=StringVar()
		self.textVar=None
		if "text" in kwargs:
			self.labelData.set(kwargs["text"])
		if "textvariable" in kwargs:
			self.textVar=kwargs["textvariable"]

		#Store colour variables
		self.colourVar=""

		#Bind label to hover functions
		if hover:
			self.bind("<Enter>",lambda event:self.hover())
			self.bind("<Leave>",lambda event:self.changeColour(self.colourVar))

	def changeColour(self,colour):
		self.config(fg=colour)
		self.colourVar=colour

	def updateText(self,newText,changeData):
		"""
		This method is used to update the text
		of the label class. It can be updated temporarily
		or not. changeData means the data in class is not changed
		"""
		if self.textVar != None:
			self.textVar.set(newText)
		else:
			self.config(text=newText)
		#If data needs to be changed or not
		if changeData:
			self.labelData.set(newText)

	def restoreData(self):
		"""
		This method will restore that data back
		to what is stored in the string var
		"""
		if self.textVar != None:
			self.textVar.set(self.labelData.get())
		else:
			self.config(text=self.labelData.get())

	def hover(self):
		currentColour=self.cget("fg")
		if currentColour == "#000000":
			self.config(fg="#FFFFFF")
		elif currentColour == "#FFFFFF":
			self.config(fg="#000000")
		else:
			self.config(fg=getColourForBackground(currentColour))

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

		#Store commands
		self.commands=[]

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
			#Run commands
			for item in self.commands:
				try:
					item()
				except:
					log.report("Error running screen command",tag="Error")
					try:
						item
					except:
						pass



	def addCommand(self,command):
		self.commands.append(command)

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

		#Track item colours
		self.colourDict={}

		#Track number of items in listbox
		self.numberOfItems=0

		#Keep status vars
		self.labelVarList=[]

		#Add a scrollbar
		self.scrollbar=Scrollbar(self)
		self.scrollbar.pack(side=RIGHT,fill=Y)

		self.scrollbar.config(command=self.yview)
		self.config(yscrollcommand=self.scrollbar.set)

	def addObject(self, textToDisplay, objectInstance, **kwargs):
		"""
		The add function allows an object
		to be added to the listbox and display plain
		text
		"""
		self.listData[textToDisplay]=objectInstance
		self.addItem(textToDisplay,**kwargs)

	def addItem(self,text,**kwargs):
		"""
		The method that actuall adds the data
		to the UI and generates a colour
		"""
		self.insert(END,text)

		#Change colour
		if text not in self.colourDict:
			colour=generateHexColour()
			if "colour" in kwargs:
				colour=kwargs["colour"]
			self.colourDict[text]=colour

		else:
			colour=self.colourDict[text]

		self.itemconfig(END,bg=colour)

		#Change FG
		try:
			fgColour=getColourForBackground(colour)
		except:
			log.report("Error getting fg colour for",colour,tag="Error",system=True)
		else:
			self.itemconfig(END,fg=fgColour)

		#Update the label
		self.updateVars("Results: "+str(len(self.get(0,END))))

	def addPodList(self,poDict):
		"""
		This method can add a dictionary of data
		pods to the listbox
		"""
		self.fullClear()
		for item in poDict:
			self.addObject(item, poDict[item])

	def getSelectedObject(self):
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

	def updateVars(self,data):
		for item in self.labelVarList:
			item.set(data)

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

	def addCertain(self,listToAdd):
		"""
		This method will take a list of text
		and if the text is a valid indicator it will add it back
		"""
		for item in listToAdd:
			if item in self.listData:
				self.addItem(item)

	def restore(self):
		"""
		Will restore all the data that was in 
		the pod list to the UI
		"""
		self.delete(0,END)
		for item in self.listData:
			self.insert(END,item)

	def clear(self):
		self.delete(0,END)

	def addLabelVar(self,source):
		if source not in self.labelVarList:
			self.labelVarList.append(source)

class advancedTree(ttk.Treeview):
	"""
	This is a modified tree view
	which will make it easier to do
	the basic operations and auto add
	scroll bar etc.
	"""
	def __init__(self,parent,columns,**kwargs):
		ttk.Treeview.__init__(self,parent,show="headings",columns=columns)
		self.columns=columns

		#Add the scrollbar
		self.scroll=Scrollbar(self)
		self.scroll.pack(side=RIGHT,fill=Y)

		self.scroll.config(command=self.yview)
		self.config(yscrollcommand=self.scroll.set)

	def addSection(self,sectionName):
		"""
		Add a section to the tree
		"""
		self.column(sectionName,width=10,minwidth=45)
		self.heading(sectionName,text=sectionName)


	def insertData(self,values,tags):
		"""
		Method to insert data into the treeview
		"""
		self.insert("" , 0,values=values,tags=tags)

	def addTag(self,tag,colour):
		self.tag_configure(tag,background=colour)

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
		self.requiredList=[]
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
		"""
		This method will allow you to add
		a frame to the popup window to view
		"""
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
		"""
		This method starts the window
		and makes sure the window is in focus
		and disables the main window 
		"""
		self.focus_set()
		self.grab_set()
		self.transient(self.root)

	def cancel(self):
		"""
		When the user clicks the "Cancel" button
		it will destroy the window and return to main window
		"""
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

	def addRequiredFields(self,entryList):
		"""
		This method will add required entries to
		the class. These are entries that need
		to have data in them
		:param entryList:
		:return:
		"""
		for item in entryList:
			self.requiredList.append(item)
	def save(self):
		"""
		The save method will collect all the data
		from the data sources and then execute the
		correct commands when the window has been
		destroyed
		"""
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

	def changeEntryColour(self,colour):
		"""
		Will change the colour of all the data sources
		in the popup window
		"""
		for entry in self.requiredList:
			entry.config(bg=colour)

#==============Master Custom Classes==============

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
		if frameToShow not in self.sections:
			self.sections.append(frameToShow)
			if "colour" in kwargs:
				frameToShow.colour(kwargs["colour"])
			frameToShow.pack(expand=True,fill=BOTH)

	def clearScreen(self):
		"""
		Will clear all the sections
		from the screen
		"""
		for item in self.sections:
			item.pack_forget()

	def showSections(self):
		self.clearScreen()
		for item in self.sections:
			item.pack(expand=True,fill=BOTH)

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
		self.topBar.colour("#C5CDCD")

		#Tracks the views
		self.views={}
		self.labelDict={}
		self.currentView=None

		self.viewCount=0

		#Colour variables
		self.selectColour="#FFFFFF"
		self.selectFG="#000000"

		self.notSelected="#98A5AA"
		self.notSelectedFG=getColourForBackground(self.notSelected)
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

			#Ensure same frame isn't loaded
			if currentViewName != name:
				if currentViewName != None:
					#Hide frame
					self.views[currentViewName].pack_forget()
					#Update label
					self.labelDict[currentViewName].config(bg=self.notSelected,fg=self.notSelectedFG)

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
		else:
			log.report("Invalid view loaded by notebook")

	def hideTab(self,name):
		"""
		This method will hide one of the tabs
		in the notebook 
		"""
		if name in self.labelDict:
			self.labelDict[name].grid_forget()

	def unHideTab(self,name):
		pass

class advancedSlider(mainFrame):
	"""
	This class is a modified scale widget.
	It will add more customization and 
	a label kwarg which adds a label to the widget
	"""
	def __init__(self,parent,text,*extra,**kwargs):

		mainFrame.__init__(self,parent)

		#Important
		self.text=text
		self.outputVar=StringVar()
		self.commands=[]

		#UI
		self.label=mainLabel(self,text=self.text)
		self.label.pack()

		self.sliderContainer=mainFrame(self)
		self.sliderContainer.pack()

		self.slider=ttk.Scale(self.sliderContainer,length=150,**kwargs)
		self.slider.grid(row=0,column=0)

		self.outputLabel=mainLabel(self.sliderContainer,textvariable=self.outputVar,width=5)
		self.outputLabel.grid(row=0,column=1)

		#Update label
		self.outputVar.set(self.getValue())

		#Adds command run
		self.slider.config(command=self.run)

	def addCommand(self,command):
		"""
		Will add a command to the list to execute
		when slider moves
		"""
		if command not in self.commands:
			self.commands.append(command)

	def run(self,value):
		"""
		THis is the method called every time the slider
		moves
		"""

		value=round(float(value))
		#Run the commands
		for command in self.commands:
			try:
				command()
			except:
				log.report("Error running command","(Slider)",tag="Error",system=True)
		#Update label
		self.outputVar.set(value)

	def getValue(self):
		return int(float(self.slider.get()))

class multiView(mainFrame):
	"""
	The multiview class is a class that allows
	multiple frames to be viewed in the same place
	by changing frames with simple methods
	"""
	def __init__(self,parent,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)

		#Stores the views
		self.views={}

		self.lastView=None
		self.currentView=None

	def addView(self,frameToShow,name):
		#Add a certain frame to the dictionary
		if name not in self.views:
			self.views[name]=frameToShow

	def showView(self,name):
		"""
		The show view method when called will show
		a certain frame in the dictionary. This value
		is referenced using an indicator string
		"""
		if name in self.views:
			if name != self.lastView:
				if self.lastView != None:
					self.views[self.lastView].pack_forget()
				self.views[name].pack(expand=True,fill=BOTH)
				self.lastView=name
		else:
			log.report("Non registered frame attempted to be show",name,tag="Error",system=True)

#==============Secondary Master Classes==============

class searchListbox(advancedListbox):
	"""
	This class will be a modified advancedListbox
	that will have a built in search bar that will
	search through its own data source and return results
	to itself
	"""
	def __init__(self,parent,**kwargs):
		advancedListbox.__init__(self,parent,font="Avenir 20",**kwargs)
		self.searchSource=None
		#Stores number of search results (-1 so it cant be same as empty search)
		self.searchNumber=-1

	def addSearchWidget(self,widget,**kwargs):
		"""
		This function will allow a search
		entry to be added to the class which
		will control all of the searching functions
		
		The result variables are string variables 
		that will update with the number of results
		the search returned
		"""
		#Add the widget to obejct
		self.searchSource=widget
		#Add a binding to self
		widget.bind("<KeyRelease>",lambda event:self.search())

		#Add the result string variables to object
		if "resultVar" in kwargs:
			resultVar=kwargs["resultVar"]
			self.addLabelVar(resultVar)
		#Report
		log.report("Added a search source to widget","(Search Listbox)")

	def search(self):
		"""
		The command that is executed when the user begins to type
		in the search source
		"""
		#Colect data
		target=getData(self.searchSource)
		dataSource=self.listData
		results=[]
		#Check though self data
		for item in dataSource:
			if advancedSearch(target,item):
				results.append(item)

		#This if statement makes sure same data is reloaded
		if len(results) != self.searchNumber:
			self.searchNumber=len(results)
			self.addSearchResults(results)

	def addSearchResults(self,results):

		#Add results
		self.clear()
		self.addCertain(results)
		#Update label
		self.updateVars("Results: "+str(len(results)))

class titleLabel(mainLabel):
	"""
	The title label is a class
	for displaying labels that
	are important
	"""
	def __init__(self,parent,**kwargs):
		mainLabel.__init__(self,parent,**kwargs)
		self.config(font=mainFont+" 17")

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

class labelEntry(mainFrame):
	"""
	This class will be an entry with a built in
	label underneath to display a certain value
	"""
	def __init__(self,parent,**kwargs):

		#Get title for object
		self.title=None
		if "title" in kwargs:
			self.title=kwargs["title"]
			kwargs.pop("title")
		#Init
		mainFrame.__init__(self,parent)

		if self.title != None:
			#Title label
			self.titleLabel=titleLabel(self,text=self.title)
			self.titleLabel.pack()

		#Create entry
		self.entry=Entry(self,**kwargs)
		self.entry.pack()

		#Create label
		self.dataVar=StringVar()
		self.dataLabel=mainLabel(self,textvariable=self.dataVar,font="Helvetica 10")
		self.dataLabel.pack()

	def insert(self,data):
		#Add data to the entry
		insertEntry(self.entry,data)

	def updateLabel(self,data):
		#Update the label with a value
		self.dataVar.set(data)

	def get(self):
		#Return value in the entry
		return self.entry.get()

	def changeColour(self,colour):
		#Change entry colour
		self.entry.config(bg=colour)

#==============Password Widget Classes==============

class privateTemplate:
	"""
	Class for storing templates 
	of display views.
	The tabData will store all the tabs
	the template will use
	and each tab will have a dictionary containing
	all the private sections it will have
	"""
	templates={}
	#Stores which colours represent which template
	templateColours={}
	def __init__(self,templateName,**kwargs):
		self.name=templateName

		if "colour" in kwargs:
			self.colour=kwargs["colour"]
		else:
			self.colour=generateHexColour()

		#Add to object array
		privateTemplate.templates[templateName]=self

		#Add to colour dict
		privateTemplate.templateColours[templateName]=self.colour
		#Stores tabs
		self.tabData={}
		self.sectionTitles=[]

		#Auto create basic and title
		self.addTab("Basic")
		self.addTemplateSection("Basic","Title",Entry)

	def addTab(self,tabName):
		"""
		This method will add a tab to the template
		for use in a notebook
		"""
		if tabName not in self.tabData:
			#Creates empty array to store sections
			self.tabData[tabName]=[]

	def addTemplateSection(self,tabIndicator,sectionTitle,sectionDataType,**kwargs):
		"""
		This method will add a section to the template
		using an indicator to determine which tab
		"""
		if tabIndicator in self.tabData and sectionTitle not in self.sectionTitles:
				self.tabData[tabIndicator].append([sectionTitle,sectionDataType,"#F7FDFF"])
				#if a colour is specified
				if "colour" in kwargs:
					self.tabData[tabIndicator][len(self.tabData[tabIndicator])-1][2]=kwargs["colour"]

	def colourSection(self,tabIndicator,sectionName,chosenColour):
		if tabIndicator in self.tabData:
			tabArray=self.tabData[tabIndicator]
			tabArray[0][2]=chosenColour

class dataSection(mainFrame):
	"""
	This class will be used to hold
	data. It will be a frame on screen
	that has a label and data source
	"""
	def __init__(self,parent,title,**kwargs):
		mainFrame.__init__(self,parent,**kwargs)
		self.title=title
		#Store data source
		self.dataSource=None
		#Store that data
		self.data=None

	def addData(self,data):
		"""
		This method adds data to the data source
		of the widget
		"""
		if self.dataSource != None:
			insertEntry(self.dataSource,data)
			self.data=data

	def getData(self):
		if self.dataSource:
			return getData(self.dataSource)
		else:
			return None

	def clearData(self):
		"""
		This method will clear all data
		in the data source
		"""
		if self.dataSource != None:
			self.enableDataSource()
			insertEntry(self.dataSource,"")
			self.data=""

	def copyData(self):
		"""
		This method will copy the data saved in the object
		to the clipboard
		"""
		addDataToClipboard(self.data)

	def restore(self):
		"""
		This method will add the saved data back
		to the data source if it was modified
		:return: 
		"""
		if self.dataSource:
			insertEntry(self.dataSource,self.data)

	def update(self):
		"""
		This method will update the
		data stored with what is in
		the entry.
		"""
		if getData(self.dataSource) != self.data:
			self.data=getData(self.dataSource)

	def disableDataSource(self):
		"""
		This method makes the data source
		un usable
		:return: 
		"""
		if self.dataSource:
			self.dataSource.config(state=DISABLED)
			if type(self.dataSource) == Text:
				self.dataSource.config(fg="grey")

	def enableDataSource(self):
		"""
		This method will allow the user
		to edit data in the data source
		"""
		if self.dataSource:
			self.dataSource.config(state=NORMAL)
			if type(self.dataSource) == Text:
				self.dataSource.config(fg="black")

class privateDataSection(dataSection):
	"""
	This class will be a data section that
	is used for storing pod info it will automatically
	create the widgets etc.
	Available sources are...
	*Entry
	*Text
	"""
	def __init__(self,parent,title,selectedSource,**kwargs):
		dataSection.__init__(self,parent,title,**kwargs)

		#Variables
		self.dataSourceType=None
		self.dataSourceWidget=None

		#State variables
		self.hidden=False

		#Track buttons
		self.buttonDict={}
		self.buttonCounter=-1

		#Ui Elements
		self.container=mainFrame(self)
		self.labelFrame=mainFrame(self.container)
		self.dataFrame=mainFrame(self.container)
		self.buttonFrame=mainFrame(self.container)

		#Create the default elements
		self.titleLabel=mainLabel(self.labelFrame,text=(self.title),width=12)
		self.titleLabel.pack(expand=True)

		"""
		This is where the layout
		will be created depending
		on what kind of data will be
		show. Entry or Text widget
		"""

		#Text or Other
		if selectedSource == Text:
			#Create data source
			dataSourceWidget=Text(self.dataFrame,height=10,font=mainFont)
			dataSourceWidget.pack(fill=X)
			self.dataSourceType=Text
			self.dataSource=dataSourceWidget
			#Create screen layout
			self.container.pack(fill=X)
			self.labelFrame.pack(side=TOP,fill=X,pady=10)
			self.dataFrame.pack(expand=True,fill=X)
			self.buttonFrame.pack(side=BOTTOM,fill=X)

		#Entry
		else:
			#Create data source
			dataSourceWidget=Entry(self.dataFrame,width=25,font=mainFont)
			dataSourceWidget.pack(expand=True)
			self.dataSourceType=Entry
			self.dataSource=dataSourceWidget

			#Create the copy button
			self.addButton("Hide",lambda: self.toggleHide())
			self.addButton("Copy",lambda: self.copyData())
			#Create screen layout
			self.container.pack(expand=True)
			self.labelFrame.pack(side=LEFT)
			self.buttonFrame.pack(side=RIGHT,padx=5)
			self.dataFrame.pack(side=RIGHT)

		if "colour" in kwargs:
			self.colour(kwargs["colour"])

	def addButton(self,title,command):
		"""
		This method will create a new button that will be displayed
		on the frame and stored in a dictionary
		"""
		self.buttonCounter+=1
		newButton=mainButton(self.buttonFrame,text=title,command=command,width=9)
		newButton.grid(row=0,column=self.buttonCounter)
		#Add to dict
		self.buttonDict[title]=newButton

	def toggleHide(self,**kwargs):

		#Override funcitons will not toggle
		if "stay" in kwargs:
			stay=kwargs["stay"]
			if stay == "hidden":
				if self.dataSourceType == Entry:
					self.dataSource.config(show="•")
					self.buttonDict["Hide"].config(text="Show")
					self.hidden=True
			elif stay == "show":
				if self.dataSourceType == Entry:
					self.dataSource.config(show="")
					self.buttonDict["Hide"].config(text="Hide")
					self.hidden=False
		else:
			if self.hidden == False:
				if self.dataSourceType == Entry:
					self.dataSource.config(show="•")
					self.buttonDict["Hide"].config(text="Show")
					self.hidden=True
			else:
				if self.dataSourceType == Entry:
					self.dataSource.config(show="")
					self.buttonDict["Hide"].config(text="Hide")
					self.hidden=False





class passwordDisplayView(displayView):
	"""
	This class is a modified display view
	and will contain special methods to add batter
	security.
	"""
	def __init__(self,parent):
		displayView.__init__(self,parent)
		#Store the sections
		self.sectionData={}

	def addPrivateSection(self,title,section):
		"""
		This method will add a private
		section to the display view and 
		store it in the object class
		"""
		self.sectionData[title]=section
		self.addSection(section)

	def disable(self):
		"""
		This method will disable editing all the 
		data in the display view
		"""
		for item in self.sectionData:
			self.sectionData[item].disableDataSource()
			#Enable the hide button
			try:
				self.sectionData[item].buttonDict["Hide"].config(state=NORMAL)
			except:
				pass
	def enable(self):
		"""
		Will enable all the sections inside
		the display view
		:return: 
		"""
		for item in self.sectionData:
			self.sectionData[item].enableDataSource()
			#Disable the hide button and ensure the data is visible
			try:
				self.sectionData[item].buttonDict["Hide"].config(state=DISABLED)
				self.sectionData[item].toggleHide(stay="show")
			except:
				pass

	def restore(self):
		"""
		This method will restore any data that
		was changed by the user when editing
		:return: 
		"""
		for item in self.sectionData:
			self.sectionData[item].restore()

	def updateAll(self):
		"""
		Bulk save all the data changed
		by the user
		:return:
		"""
		for item in self.sectionData:
			self.sectionData[item].update()


	def configAllButtons(self,buttonName,state):
		"""
		This method will disable or enable
		all the buttons with a certain title
		in the display view
		"""
		for section in self.sectionData:
			#Goes through all the buttons
			for button in self.sectionData[section].buttonDict:
				if button == buttonName:
					if state == "DISABLED":
						self.sectionData[section].buttonDict[button].config(state=DISABLED)
					else:
						self.sectionData[section].buttonDict[button].config(state=NORMAL)



	def fullClear(self):
		for item in self.sectionData:
			self.sectionData[item].clearData()
			
class privateNotebook(advancedNotebook):
	"""
	This class will be used on the view pod
	screen and will display the data from a pod
	"""
	def __init__(self,parent,**kwargs):
		advancedNotebook.__init__(self,parent,**kwargs)


		#Create the strip along the top
		self.templateStrip=mainFrame(self)
		self.templateStrip.pack(side=TOP,fill=X)

		#The strip that shows which template is loaded
		self.templateLabelVar=StringVar()
		self.templateLabelVar.set("No template loaded")

		self.templateLabel=mainLabel(self.templateStrip,textvariable=self.templateLabelVar)
		self.templateLabel.pack(expand=True)

		#Colour the template strip
		self.templateStrip.colour("#8E9193")
		#Stores display views and tabs
		self.tabDict={}
		#Which data should be hidden by default
		self.privateData=["Password"]
		#Store the last template so same are not reloaded
		self.lastTemplate=None
		#Stores the multi view instance
		self.multiViewInstance=None

		#Store the first tab added
		self.firstTab=None

		#Create Basic And Advanced
		self.addNewDisplayTab("Basic")
		self.addNewDisplayTab("Advanced")

	def addNewDisplayTab(self,tabName):
		"""
		This method will create a new display view
		and create a new tab for it
		"""
		if tabName not in self.tabDict:
			#Create the display view
			newDisplay=passwordDisplayView(self)
			self.addView(newDisplay,tabName)
			self.tabDict[tabName]=newDisplay
			#Attempt to update var
			if self.firstTab == None:
				self.firstTab=tabName
			return newDisplay
		else:
			return self.tabDict[tabName]

	def getDisplay(self,indicator):
		"""
		This method will return the display view
		that was created when a new tab was added
		"""
		if indicator in self.tabDict:
			return self.tabDict[indicator]

	def loadTemplate(self,templateName):
		log.report("Loading template",templateName)
		#todo add better efficiency here
		if templateName != self.lastTemplate:
			if templateName in privateTemplate.templates:

				#First Clear the screen
				for tab in self.tabDict:
					self.tabDict[tab].clearScreen()


				#Update the template label var
				self.templateLabelVar.set(templateName)

				template=privateTemplate.templates[templateName]
				for tab in template.tabData:
					tabArray=template.tabData[tab]
					display=self.addNewDisplayTab(tab)
					if display != None:
						for item in tabArray:
							newPrivateSection=privateDataSection(display,item[0],item[1],colour=item[2])
							display.addPrivateSection(item[0],newPrivateSection)


				#Update last template var
				self.lastTemplate=templateName
			else:
				log.report("Unable to load template could not find name",templateName)

	def loadDataPod(self,dataPodInstance):
		"""
		This methos is used to load a data pod
		onto the notebook. It will take the pod 
		vault and display it on screen
		"""
		if type(dataPodInstance) == PEM.dataPod:

			#Get the type of pod
			templateType=dataPodInstance.templateType
			#Load the correct template
			if templateType in privateTemplate.templates:
				self.loadTemplate(templateType)

			#Load default template
			else:
				log.report("Invalid template name to load",templateType)
				self.loadTemplate("Login")

			#Clear the screen
			for display in self.tabDict:
				self.tabDict[display].fullClear()
			#Make sure edit mode is turned off
			self.multiViewInstance.showView("Edit")

			#Get the pod vault
			podVault=dataPodInstance.podVault

			#Add title separately
			if "Title" not in podVault:
				self.tabDict["Basic"].sectionData["Title"].addData(dataPodInstance.podName)
			#Add the data
			for display in self.tabDict:
				for section in self.tabDict[display].sectionData:
					if section in podVault:
						#Add to entry
						self.tabDict[display].sectionData[section].addData(podVault[section])
						self.hidePrivateData()

			#Ensure the first tab is loaded
			self.showView(self.firstTab)

			#Disable editing
			for item in self.tabDict:
				self.tabDict[item].disable()

	def startEdit(self):
		"""
		This method will start edit mode. This will
		allow the user to change pod data
		and edit it and save it or cancel
		"""
		if self.multiViewInstance:
			if type(self.multiViewInstance) == multiView:
				#Change mutiview
				self.multiViewInstance.showView("Cancel")
				#Make the data editable
				for item in self.tabDict:
					self.tabDict[item].enable()

	def cancelEdit(self):
		"""
		This is the method that will be called 
		when the user chooses to cancel the edit.
		It will restore the data if the user changed it
		and return to default
		"""

		if self.multiViewInstance:
			#Change mutiview
			self.multiViewInstance.showView("Edit")
			#Disable the data
			for item in self.tabDict:
				self.tabDict[item].restore()
				self.tabDict[item].disable()
				#Hide private data
				self.hidePrivateData()

		if self.multiViewInstance:
			if type(self.multiViewInstance) == multiView:
				#Change mutiview
				self.multiViewInstance.showView("Edit")
				#Disable the data
				for item in self.tabDict:
					self.tabDict[item].restore()
					self.tabDict[item].disable()

	def saveData(self):
		"""
		This method is used to save the new data
		entered in the data sources for the notebook
		:param multiViewInstance:
		:return:
		"""
		#Updates the pod vault
		currentMasterPod=PEM.masterPod.currentMasterPod
		if currentMasterPod:
			#Get the data pod that is currently loaded
			currentPod=PEM.masterPod.currentMasterPod.currentPod
			if currentPod:
				#Find changed data
				for display in self.tabDict:
					for section in self.tabDict[display].sectionData:
						hiddenSection=self.tabDict[display].sectionData[section]
						if hiddenSection.getData != hiddenSection.data:
							#Find coresponding pod
							currentPod.updateVault(section,hiddenSection.getData())

							#todo if title is changed update listbox
			#Save the data
			for tab in self.tabDict:
				self.tabDict[tab].updateAll()
			#Cancel the edit
			self.cancelEdit()
			#Save to file
			currentMasterPod.save()




		else:
			askMessage("No pod","No master pod has been loaded")

	def hidePrivateData(self):
		#Make sure private data is hidden by default
		for display in self.tabDict:
			for section in self.tabDict[display].sectionData:
				if section in self.privateData:
					self.tabDict[display].sectionData[section].toggleHide(stay="hidden")


#==============Other Classes==============



#===============================(Private Templates)===============================

"""
Private templates are templates for storing pod data
they contain the relevant information to create widgets
that can hold different data.
Some examples of templates include...
*Logins
*Notes
*Bank details
"""
#===Normal Login===
privateLoginTemplate=privateTemplate("Login")
privateLoginTemplate.addTab("Advanced")
privateLoginTemplate.colourSection("Basic","Title","#67A1FF")
privateLoginTemplate.addTemplateSection("Basic","Username",Entry,colour="#5C90E3")
privateLoginTemplate.addTemplateSection("Basic","Password",Entry,colour="#5382CE")

privateLoginTemplate.addTemplateSection("Advanced","Website",Entry,colour="#55CEC3")
privateLoginTemplate.addTemplateSection("Advanced","Notes",Text,colour="#4DBCB2")

#===Secure Note===
privateSecureNote=privateTemplate("Secure Note")
privateSecureNote.colourSection("Basic","Title","#6ECA3F")
privateSecureNote.addTab("Advanced")
privateSecureNote.addTemplateSection("Advanced","Notes",Text,colour="#55CA88")