#! /usr/bin/env python3.0

#Monty Shell
#Adam Traub

"""
Monty is a python based Linux shell.  It features high level
object orientation and utilizes python's ease of use with lists
and class design.
"""
import os
import sys
from signal import *

"""
The Executer class is in charge of executing the 
non-internal commands.  
"""
class Executer:
	def __init__(self,table):
		self.table = table #The table of background processes
		self.pipeVals = [] #What are the piping values

	def execute(self,argsx,oArgs):	
		self.pipeVals = []
		
		"""
		Get all the pipe values from all the pipes in 
		the given set of arguments.
		"""
		for args in argsx:	
			self.pipeVals += args.getCVals()

		"""
		Handles the execution of the given command.
		"""
		for index in range(len(argsx)):
			pid = os.fork()

			if pid == -1:
				sys.stderr.write("Fork Failed!")
				exit(1)

			#Parent
			elif pid != 0:
				pass 
				
			#Child
			elif pid == 0:		
				signal(SIGINT, SIG_DFL) #Allows Ctrl-C to kill child
				try:
					"""
					Handles changing the piping table to account for
					piping and redirection.
					"""
					argsx[index].handleDuping() 
					for vals in self.pipeVals:
						#closes all the pipes in the child process
						os.close(vals)
						
					#Attempt to exectue the command
					os.execvp(argsx[index].getLocation(), argsx[index].getArgument())

				#What to do if command is not found.
				except OSError as a:	
					print("Monty: "+argsx[index].getLocation()+": command not found")

				#closes the child process (if os.execvp didn't do so)
				finally:			
					exit(1)

		#closes all the pipes in the parent's process table
		for items in self.pipeVals:
			os.close(items)
		
		"""
		Handles adding the background process to the background
		process table and then continues without waiting for
		background processes.
		"""
		if argsx[0].isBackground():
			self.table.append([pid,oArgs])
			print(self.table.IDandPos(pid,len(self.table)))
			os.waitpid(pid,os.WNOHANG)

		#Wait for all child processes to complete.
		else:
			for i in range(len(argsx)):
				os.wait()
					
	#debug method to get piping values.
	def getPipeVals(self):
		return self.pipeVals


"""
The Splitter gets user input and turns
the items into Argument objects.
"""
class Splitter:
	def __init__(self,fileLocation, hist, delim =" "):
		self.fileLocation  = fileLocation #Location of history file
		self.hist          = hist #command history
		self.delim         = delim #delimiter used for string splitting
		self.workingString = "" #The unsplit String of commands
		self.workingList   = [] #The list of commands

	#Creates the command prompt
	def makePrompt(self):
		name     = os.getlogin() #username
		terminal = os.uname()[1].split(".")[0] #name of machine
		dir      = os.getcwd().split("/")[-1] #current directory

		#incase the directory is root
		if dir == "":
			dir = "/"
			
		prompt   = "/V\ %s@%s %s $ " %(name,terminal,dir)
		       #The /V\ symbol is an M for Monty
		return prompt

	"""
	Displays the command prompt and retrieves user input
	if the user only typed in white space, a value of None
	is returned.
	"""
	def nextCmd(self):
		try:
			#Gets the user input using the command prompt
			self.workingString = input(self.makePrompt())
			
			#Gets rid of excess spaces
			self.workingString = self.workingString.rstrip()
			self.workingString = self.workingString.lstrip()
			
			#If there was a command, add it to the command History
			if len(self.workingString) > 0:
				self.hist.append(self.workingString+"\n")
			else:
				return None
				
			#Splits the string into a list of strings split on the spaces
			retList = self.workingString.split(self.delim)
			for index in range(len(retList)):
				if not (retList[index].isspace() or retList[index] ==""):
					self.workingList.append(retList[index])

			#Turns that list of Strings into an Argument object
			if len(self.workingList) > 0:
				retArg = Argument(self.workingList)
				#Checks and sets the background flag
				if self.workingList[-1] == '&':
					retArg.setBackground(True)
					retArg.setArgument(self.workingList[:-1])
				return [retArg]
			else:
				return None
			
		#Handles CRTL-D
		except EOFError:
			terminate(self.fileLocation,self.hist)

	"""
	Get the list of commands the user typed in.  Mainly a
	debugging tool.
	"""
	def getList(self):
		return self.workingList

	"""
	Resets the workingList and workingString variables in
	order to make them empty for the next user argument.
	"""
	def reset(self):
		self.workingList = []
		self.workingString = ""

"""
Does a preprocessing of the data and prepares it for the
Executer.  It also handles builtin commands and user defined
library commands.
"""
class Processor:
	def __init__(self, fileLoc, hist, lib,table):
		self.table        = table #Background process table
		self.fileLocation = fileLoc #history file location
		self.hist         = hist #command history
		self.exe          = Executer(table) #The Executer
		self.lib          = lib #The location of the user defined library
		self.libFiles     = os.listdir(lib) #A listing of all files in the library
	

	"""
	The master method of the Processer.  It gets the Arguments ready
	for the executer and handles the library and builtin commands.
	"""
	def process(self, args):
		oArgs = args[0].getArgument() #Original argument before processing
		self.preProcess(args) #Check for piping and redirection
		currentArg = args[0].getArgument()
		rmList = [] 
		x = self.checkILibrary(args) #Check the builtin library
		
		#Changes oArgs if a history command was used.
		if x != None: 
			oArgs = x

		self.checkELibrary(args) #Check the user defined library
		
		#give the remaining arguments to the executer
		if len(args) > 0:
			self.exe.execute(args,oArgs)			

	#Checks to see if the command resides in the user defined library
	def checkELibrary(self, args):
		for index in range(len(args)):
			if args[index].getLocation().lower() in self.libFiles:
				args[index].setLocation(self.lib+
				"/"+args[index].getLocation().lower())

	#Checks to see if the command is built into the shell
	def checkILibrary(self,args):
		ret = None
		"""
		Check to see if the given command matches one of the builtin
		commands and handle accoringly.
		"""
		for x in range(len(args)):
			#View all currently running jobs
			if args[x].getLocation().lower() == "jobs":
				self.jobs()
				args.pop(x)

			#Change directory
			elif args[x].getLocation().lower() == "cd":
				self.cd(args[x])
				args.pop(x)

			#See how many BKGD jobs have been ran since the start
			#of this session and how many are currently running
			elif args[x].getLocation().lower() == "jobcount":
				self.jobCount()
				args.pop(x)

			#!!x
			#Perform the command that was performed x number of
			#commands ago.
			elif args[x].getLocation()[:2] == "!!":
				ret = self.utilNHistory(args,x)
				self.checkILibrary(args)

			#!x
			#Perform the last command that starts with character/s (x)
			elif args[x].getLocation()[0] == "!":
				ret = self.utilHistory(args,x)
				self.checkILibrary(args)

			#Terminate
			elif args[x].getLocation().lower() in ["exit","quit"]:
				terminate(self.fileLocation,self.hist)
				
				
		return ret
				
	#Builtin Command: Change Directory
	def cd(self, args):
		try:
			os.chdir(args.getArgument()[1])
		except IndexError:
			print("cd needs more arguments!\n")
		except OSError:
			print("No such directory!\n")

	"""
	Builtin Command: !! -  This syntax for the command is
	!!x where x is an integer.  If used correctly it will execute the
	command that was performed x steps ago.
	"""
	def utilNHistory(self,args,index):
		try:
			arg = args[index]
			num = len(self.hist) - int(arg.getLocation()[2:])
			if num < 0:
				raise ValueError
			newArg = self.hist[num].split()
			print(self.hist[num])
			self.preProcess(args)
			return self.hist[num]
			
		#Exception thrown if X is too large.
		except IndexError:
			newArg = ("echo Monty: Index out of range: %s" %(arg.getLocation()[2:])).split()
		#Exception thrown if X is not an integer.
		except ValueError:
			newArg = ("echo Monty: Improper Value: \"%s\"  Must be a positive integer" %(arg.getLocation()[2:])).split()
			
		finally:
			arg.setArgument(newArg)
			arg.setLocation(newArg[0])
			if arg.getArgument()[-1] == "&":
				arg.setArgument(x[:-1])
				arg.setBackground(True)
			
	"""
	Builtin Command: ! - The proper syntax is !x where x is the
	beginning of a previous command.  If used correctly it will
	find the associated command and execute it accordingly.
	"""
	def utilHistory(self,args,index):
		arg = args[index]
		loc = arg.getLocation()[1:]
		siz = len(loc)
		for index in range(len(self.hist)-1,-1,-1):
			if self.hist[index][:siz] == loc:
				x = self.hist[index].split()
				arg.setArgument(x)
				arg.setLocation(x[0])
				if arg.getArgument()[-1] == "&":
					arg.setArgument(x[:-1])
					arg.setBackground(True)				
				print(self.hist[index])
				self.preProcess(args)
				return self.hist[index]
		newArg = ("echo Monty: %s: Event not found!" %(arg.getLocation())).split()
		arg.setArgument(newArg)
		arg.setLocation(newArg[0])
		
				
	"""
	The builtin Command: Jobs - This command will show
	all currently running background jobs.
	"""
	def jobs(self):
		x = self.table.__str__()
		if not self.table.isEmpty():		
			print(self.table)


	"""
	The builtin Command: jobCount - This command will display
	the number of background processes currently running and the
	number that have been ran since the shell started. The command
	is not case sensitive.
	"""
	def jobCount(self):
		ret = """
Number of background Processes
Currently running:     %i
Ran since shell start: %i
"""%(len(self.table),self.table.totalEver())
		print(ret)

	
	#Checks for piping and redirection with a tail end recursion.
	def preProcess(self, argList, num=0):
		currentArg = argList[num]
		args = currentArg.getArgument()
		retArgs = args
		for eachArg in range(len(args)):
			#redirect stdout write only
			if args[eachArg] == ">":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_WRONLY))
				retArgs = retArgs[:eachArg]+args[eachArg+2:]
				currentArg.setWrite(fnum)
				currentArg.setArgument(retArgs)

			#redirect stdout append
			elif args[eachArg] == ">>":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_APPEND))
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setWrite(fnum)
				currentArg.setArgument(retArgs)
		
			#redirect stderr wronly
			elif args[eachArg] == "2>":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_WRONLY))
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setErr(fnum)
				currentArg.setArgument(retArgs)
				
			#redirect stderr append
			elif args[eachArg] == "2>>":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_APPEND))				
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setErr(fnum)
				currentArg.setArgument(retArgs)

			#redirect stdout to stderr
			elif args[eachArg] == "1>&2":
				currentArg.setWrite(2)
				retArgs = retArgs[:eachArg]	
				currentArg.setArgument(retArgs)
			
			#redirect stderr to stdout
			elif args[eachArg] == "2>&1":
				currentArg.setErr(1)
				retArgs = retArgs[:eachArg]	
				currentArg.setArgument(retArgs)
				
			#switch stdout and stderr
			elif args[eachArg] in ["1><2","2><1","1<>2","2<>1"]:
				currentArg.setWrite(2)
				currentArg.setErr(1)
				retArgs = retArgs[:eachArg]
				currentArg.setArgument(retArgs)
				
			#redirect stderr and stdout write only
			elif args[eachArg] == "&>":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_WRONLY))				
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setWrite(fnum)
				currentArg.setErr(fnum)
				currentArg.setArgument(retArgs)

			#redirect stderr and stdout append
			elif args[eachArg] == "&>>":
				fnum = os.open(args[eachArg+1],(os.O_CREAT | os.O_APPEND))
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setWrite(fnum)
				currentArg.setErr(fnum)
				currentArg.setArgument(retArgs)


			#redirect stdin 
			elif args[eachArg] == "<":
				fnum = os.open(args[eachArg+1],os.O_RDONLY)
				retArgs = retArgs[:eachArg]+args[eachArg+2:]	
				currentArg.setRead(fnum)
				currentArg.setArgument(retArgs)
		
			#OR operation
			elif args[eachArg] == "||":
				read,write,err,isBack = currentArg.getAllVals()
				currentArg.setArgument(retArgs[:eachArg])
				args2 = Argument(retArgs[eachArg+1:])
				args2.setBackground(isBack)
				argList.append(args2)
				self.preProcess(argList,num+1)
				return
				
			
			#Pipe O-O
			elif args[eachArg] == "|":
				read,write,err,isBack = currentArg.getAllVals()		
				currentArg.setArgument(retArgs[:eachArg])			
				currentArg.setPipesOutput(True)
				args2 = Argument(retArgs[eachArg+1:])
				args2.setBackground(isBack)
				readEnd,writeEnd = os.pipe()
				currentArg.setWrite(writeEnd)
				args2.setRead(readEnd)			
				argList.append(args2)
				self.preProcess(argList,num+1)
				return

"""
The Background process table keeps track of all background processes.
When a job is completed, its spot in the table is replaced by a value
of None.  At surface glance, this may sound bad since the size of the
table could theoretically get so large that the machine may run out of
memory, however, testing showed that a list could contain over
300,000,000 elements without causing any issues.
"""
class BackgroundProcessTable:
	#An entry is a list with a pid and a list of arguments
	def __init__(self):
		self.table = [] #An underlying list to hold the job entries

	#A toString method to properly display the Table
	def __str__(self):
		retString = ""
		jobList = []
		for items in self.table:
			if items == None:
				jobList.append(None)
				continue
			tempString = ""
			for args in items[1]:
				tempString += args+" "
			jobList.append(tempString)

		for index in range(len(self.table)):
			if self.table[index] == None:
				continue
			retString+= "[%d] %d          %s" %((index+1),self.table[index][0],
			jobList[index])
			if index < len(self.table)-1:
				retString += "\n"
		return retString

	#given an item and an index, this method shows the proper output
	def itemToString(self,index,item):
		jobString = ""
		for dex in range(0,len(item[1])):
			jobString += item[1][dex]+" "
		return "[%d]+ Done          %s" %((index+1), jobString)
			
	#Another printing utility method.
	def IDandPos(self,id,spot):
		return "[%d] %d" %(spot, id)
		
	#Check to see if the command completed.
	#WARNING: This method has a bug.
	def check(self):
		retString = ""
		newList = list(self.table)
		
		try:
			for index in range(len(newList)):
				if newList[index] == None:
					continue
				id = newList[index][0]
				pid, status = os.waitpid(id,os.WNOHANG)
				if pid != 0:
					retString += self.itemToString(index, newList[index])+"\n"
					self.table[index] = None
		
		except OSError as a:
			#This catches the bug, but it's only a band-aid, not a proper
			#solution
			errString = """   You've found the one bug I still know of, this bug
   seems to occur when a background process and a foreground
   process have the same location. I do not understand why an
   error such as this would occur, therefore my efforts to debug
   it thus far have failed."""
			
			print(errString)
			print(a)
		
		finally:
			return retString[:-1]

	#The number of currently running background processes
	def __len__(self):
		x = 0
		for items in self.table:
			if items != None:
				x+=1
		return x

	#allows the notation of   y = table[key]
	def __getitem__(self,key):
		return self.table[key]
	
	#allows the notation of table[key] = value
	def __setitem__(self,key,value):
		self.table[key] = value

	#removes the item at the spot position
	def pop(self, spot=0):
		return self.table.pop(spot)

	#returns true if i is in the table
	def __contains__(self,i):
		return self.table.__contains__(i)

	#Allows += notation
	def __iadd__(self,other):
		self.table += other

	#Total background processes since shell start
	def totalEver(self):
		return len(self.table)

	#add item to end of table
	def append(self, other):
		self.table.append(other)

	#insert item i at position j
	def insert(self,i,j):
		self.table.insert(i,j)

	#remove the item at position x
	def remove(self,x):
		self.table.remove(x)

	#creates an iterator typically used for loops
	def __iter__(self):
		return self.table.__iter__()

	#resets table
	def clear(self):
		self.table = []

	#Checks to see if there are any backrgound processes
	def isEmpty(self):
		return self.__len__() == 0

#Acts as a history
class History:
	def __init__(self):
		self.hist = []
	
	#String representation of history
	def __str__(self):
		retString = ""
		for index in range(len(self.hist)):
			retString += "%i: %s\n"%(index, self.hist[index])
		return retString

	#adds a command to the list
	def append(self,item):
		#Don't add spaces
		if item.isspace():
			return
			
		#Check to see if the command is already in the list
		#If it is, remove it
		for index in range(len(self.hist)):
			if self.hist[index] == item:
				self.hist.pop(index)
				break

		#Don't add history commands
		if item[0] != "!":
			self.hist.append(item)
		
		#Make sure the length maxes at 100
		if len(self.hist) > 100:
			self.hist.pop(0)
		return

	"""
	A function to get a portion of the command history and return it
	as a String.
	This may be useful later on.
	"""
	def getSectionS(self, start=0, end=-1, count=1):
		retString = ""
		if end < 1:
			end = len(self.hist)
			
		if count < 1:
			count = 0-count
			
		if count == 0:
			count = 1
		try:
			for index in self.hist(start,end,count):
				retString += "%i: %s\n"%(index, self.hist[index])
		
		except IndexError:
			pass

		finally:
			return retString

	"""
	A function to get a portion of the command history and return it as
	a List.
	This may be useful later on.
	"""
	def getSectionL(self, start=0, end=-1, count=1):
		retList = []
		if end < 1:
			end = len(self.hist)
			
		if count < 1:
			count = 0-count
			
		if count == 0:
			count = 1
		try:
			for index in self.hist(start,end,count):
				retList.append(["%i: %s"%(index, self.hist[index])])
		
		except IndexError:
			pass

		finally:
			return retList


	"""
	A faster and simpler function used for Adding the commands 
	from the history file. The commands must be in a list.
	WARNING: THERE IS NO FILTERING, ONLY USE WHEN THE STRINGS IN THE
	LIST ARE COMPRISED OF PREVIOUS, NON-REPEATING COMMANDS. THIS CAN
	MESS UP THE COMMAND HISTORY IF ABUSED.
	"""
	def add(self,other):
		self.hist += other

	#Python builtin command used for iterating
	def __iter__(self):
		return self.hist.__iter__()

	#length of command List
	def __len__(self):
		return len(self.hist)

	#get command at position key
	#Allows History[key] notation
	def __getitem__(self,key):
		return self.hist[key]
		
"""
The Argument class is used to simplify arguments into objects that
have read,write, and err ends.  The Arguemnts are aware whether or not
their output is piped, although in the current implementation this
feature is not used.  Commands also know their Location, arguments,
and whether they are background processes or not.
"""		
class Argument:
	def __init__(self, argument, read = 0, 
	write = 1, err = 2, background = False):
		self.argument = argument
		self.location = argument[0]
		self.read  = read
		self.write = write
		self.err   = err
		self.isBackgroundP = False
		self.pipesOutput   = False

	#String representation of a command, useful in debugging
	def __str__(self):
		retString = """
Argument  :  %s
Location  :  %s
Read      :  %i
Write     :  %i
Err       :  %i
Background:  %s
Pipes Out :  %s
		""" %(str(self.argument),self.location,self.read,
		self.write,self.err,str(self.isBackgroundP), str(self.pipesOutput))
		return retString
		
	#Gets read/write/err values of the Argument if there is redirection
	#or piping.
	def getCVals(self):
		toRet = []
		if self.read >  2:
			toRet.append(self.read)
		if self.write > 2:
			toRet.append(self.write)
		if self.err > 2:
			toRet.append(self.err)
		return toRet

	#Returns read,write,err,and background
	def getAllVals(self):
		return self.read,self.write,self.err,self.isBackgroundP

	#Takes care of the duping (necessary for redirection)
	def handleDuping(self):
		os.dup2(self.read, 0)
		os.dup2(self.write,1)
		os.dup2(self.err,  2)
	
	#Accessors and Mutators

	#val must be a boolean
	def setPipesOutput(self,val=True):
		self.pipesOutput = val
	
	def isPipingOutput(self):
		return self.pipesOutput == True

	def getWrite(self):
		return self.write
	
	def isBackground(self):
		return self.isBackgroundP
		
	def setBackground(self,val=True):
		self.isBackgroundP = val
	
	def getRead(self):
		return self.read
	
	def getErr(self):
		return self.err

	def getLocation(self):
		return self.location

	def getArgument(self):
		return self.argument

	def setWrite(self,value):
		self.write = value
	
	def setRead(self,value):
		self.read = value

	def setErr(self, value):
		self.err = value

	def setArgument(self, argument):
		self.argument = argument
	
	def setLocation(self, location):
		self.location = location




#A command of "quit" or "exit" will exit the shell
def main():
	fls = "./.montyFiles" #Command history location
	lib = "./.montyLib" #User command location
	hist = History() #History
	hist.add(setup(fls,lib)) #Adds previous histories
	table = BackgroundProcessTable() #Creates BKGD Process table
	proc = Processor(fls,hist,lib,table) #Creates processor
	sp = Splitter(fls,hist) #Creates Splitter
	
	while True:
		#check table for completion of BKGD processes
		complete = table.check()
		if len(complete) > 0:
			print(complete)

		#Gets next user command
		commands = sp.nextCmd()
		
		#Don't bother processing it if it's blank
		if commands == None:
			continue
		
		#Process the commands
		p = proc.process(commands)
		
		sp.reset()#reset the splitter (could probably be written out.)
		
		
def setup(fileLoc,lib):
	#Ignore signals
	signal(SIGINT, SIG_IGN)
	signal(SIGQUIT, SIG_IGN)

	if os.path.exists(lib) == False:
		os.mkdir(lib)

	if os.path.exists(fileLoc) == False:
		os.mkdir(fileLoc)
	
	try:
		#gets history
		f = open(fileLoc+"/histList","r")
		x = f.readlines()
		f.close()
		
	except IOError:
		#If first use, make a blank table
		x = []
		
	finally:
		return x

#Commands to run on exit.
#Currently writes out history and exits
def terminate(fileLoc,hist,cause=1):
	f = open(fileLoc+"/histList","w")	
	f.writelines(hist)	
	f.close()
	print("exit")
	sys.exit(cause)
	
	
if __name__ == "__main__":
	sys.exit(main())


