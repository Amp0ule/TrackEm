import os
import subprocess 
import telegram
import time
import urllib.request
from datetime import datetime
from datetime import timedelta


def CheckForMacs(BotObj, ChatID):
	file = open("MACs.txt")
	time.sleep(2)
	for i in file:
		print(i)
		time.sleep(1)
		BotObj.sendMessage(chat_id=ChatID, text=i)

# Function : Check if there are any known Mac adress already
# Para : Bot Obj && Chat ID
# Return : Mac Known | Empty
# def CheckForKnownMac(BotObj, ChatID):
	
# Function : add news Mac Adress to the list
# Para : None
# Return : None
def addList(Msg, BotObj, ChatID):
	#if Msg == "y":
	#	BotObj.sendMessage(chat_id=ChatID, text="Ok, adding everything")
	#else: 
	#	BotObj.sendMessage(chat_id=ChatID, text="add all? (y/n)")
	#	print("Try") 
	#	answer = checkAdd(BotObj, ChatID)
	os.system('cp MACs.txt Known.txt')
	print("Copying Mac into Known")


# Function : printing list of known adress
# Para : None
# Return : String
def getKnown():
	filename = "Known.txt"
	if os.path.isfile(filename):
		return getScannedMacs(filename)
	else:
		print("Empty")

def checkAdd(bot, update_id):
	print("Hello")
	for update in bot.getUpdates(offset=update_id, timeout=10):
		chat_id = update.message.chat_id
		update_id = update.update_id + 1
		message = update.message.text
		if message:
			addList(message, bot, chat_id)
	return update_id

def clearList():
	os.system('rm Known.txt')
	print('delete Known.txt : OK')
	
def trackEm(bot, update_id):
	for update in bot.getUpdates(offset=update_id, timeout=10):
		chat_id = update.message.chat_id
		update_id = update.update_id + 1
		message = update.message.text
		if message:
			CheckAndAnswer(message, bot, chat_id)
	return update_id

def checkForList(BotObj, ChatID):
	file = open("MACs.txt")
	for i in file:
		BotObj.sendMessage(chat_id=ChatID, text=i)


def checkDiff():
	os.system("diff MACs.txt Known.txt | grep -E '<' > diff.txt")
	print("Check diff : OK")

def readDiff():
	devicediff = ""
	filesize = os.path.getsize("diff.txt")
	if filesize == 0:
		devicediff = "Nothing to check"
	else:
		file = open("diff.txt")
		for i in file:
			print(i)
			devicediff += i
	return devicediff


# Function : Read the file and make a string from the list
# Para : the list of mac adress
# Return : String of macs adress
def readMacs(macs):
	filename: "known.txt"
	devicesinrange = []
	for x in range(0, len(macs)):
		devicesinrange.append(str(x) + " -  " +  macs[x])
	devicesinrange.append(" ")
	devicesinrangestring = "\n".join(devicesinrange)
	return devicesinrangestring

			
# Function : Opening the file / reading / spliting
# Para : none
# Return ReadMacs()
def getScannedMacs(filename):
	originalMacs = open(filename).read().splitlines()
	macs = list(set(originalMacs))#No double with set
	return readMacs(macs)


# Function : Check if the file of the mac adresses exist
# Para : None
# Return : GetScannedMacs() || String -> if not found
def checkForMacFile():
	filename = "MACs.txt"
	if os.path.isfile(filename):
		return getScannedMacs(filename)
	else:
		print("Could not find the MACs.txt file")


# Function : lunch arp-scan to detect devices connected on the network
# Para : None
# Return : CheckForMacFile()
def scan():
	try:
	   os.remove('MACs.txt')
	except OSError:
		pass
	os.system('sudo arp-scan -l | grep ^[0-9][0-9] >>  MACs.txt')
	return checkForMacFile()
	

# Function: start the scan programm
# Para : none
# Return : scan() 
def start():
	print("starting scan")
	return scan()

# Function : Check the answers form the chat bot
# Para : Message, Objet Bot, Chat ID -> Bot components
# Return : answers
def CheckAndAnswer(Msg, BotObj, ChatID):
	MsgLowerCase = Msg.lower()
	if MsgLowerCase == "/start":
		print("/start command received")
		BotObj.sendMessage(chat_id=ChatID, text="Welcome to Trackem v1.2! \n") 
		time.sleep(1)
		BotObj.sendMessage(chat_id=ChatID, text="Would you like to scan for devices ? (Yes or /scan)")
		time.sleep(1)
		BotObj.sendMessage(chat_id=ChatID, text="/help for any help")
		return
	if (MsgLowerCase == "yes") or (MsgLowerCase == "/scan"):
		print("/scan command received, scanning")
		BotObj.sendMessage(chat_id=ChatID, text="Ok, let's go for a quick scan!")
		time.sleep(1)
		devicesarround = start() #start the scan
		print("Scan complete")
		try:
			now = datetime.now() + timedelta(seconds=3600)
			date_time = now.strftime("%d/%m/%Y, %H:%M:%S")
			BotObj.sendMessage(chat_id=ChatID, text="Scan complete: " + date_time + "\n" + devicesarround)
			#print(BotObj, ChatID)
			#CheckForMacs(BotObj, ChatID)
		except TypeError:
			BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n" + "No devices")
		return
	if(MsgLowerCase == "/add"):
		BotObj.sendMessage(chat_id=ChatID, text="Adding everything to the list...")
		time.sleep(1)
		addList(Msg, BotObj, ChatID)
		BotObj.sendMessage(chat_id=ChatID, text="Done")
		return
	if(MsgLowerCase == "/check"):
		BotObj.sendMessage(chat_id=ChatID, text="Checking...")
		time.sleep(1)
		checkDiff()
		check = readDiff()
		print(check)
		try:
			BotObj.sendMessage(chat_id=ChatID, text="Check done: \n" + check)
		except TypeError:
			BotObj.sendMessage(chat_id=ChatID, text="Check done: \n" + "Nothing to check")
		return 
	if(MsgLowerCase == "/quit"):
		BotObj.sendMessage(chat_id=ChatID, text="Cya!")
		return 
	if(MsgLowerCase == "/list"):
		BotObj.sendMessage(chat_id=ChatID, text="Retrieving the list of well-known devices...")
		time.sleep(1)
		listarround = getKnown()
		print("getting the known")
		try:
			print("Ok I'll try")
			BotObj.sendMessage(chat_id=ChatID, text="Here is the list: \n" + listarround)
		except TypeError:
			print("Error")
			BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n" + "Empty")
		return
	if(MsgLowerCase == "/help"):
		BotObj.sendMessage(chat_id=ChatID, text="Here is the list of cmd you can use : \n" + 
												"/start : start the bot \n" + 
												"/scan : scan the devices on your network \n" + 
												"/list : retrieve the devices known on the network \n" + 
												"/add : add new devices to the list \n" +
												"/check : check who is up on your network \n" +
												"/clear + [list/chat/...] : clearing the element \n"
+
												"/quit : stop the bot")
		return
	if(MsgLowerCase == "/clear list"):
		BotObj.sendMessage(chat_id=ChatID, text="Clearing the list...")
		clearList()
		BotObj.sendMessage(chat_id=ChatID, text="All clear!")
		return
	else:
		BotObj.sendMessage(chat_id=ChatID, text="Unknown command. /help if needed.")


update_id = None

BotToken = ""

bot = telegram.Bot(BotToken)
print("TrackEm started!")

while True:
	try:
		update_id = trackEm(bot, update_id)
	except telegram.TelegramError as e:
		if e.message in ("Bad Gateway", "Timed out"):
			sleep(1)
		else:
			raise e
