import os
import subprocess 
import telegram
import time
import urllib.request


def CheckForMacs(BotObj, ChatID):
	file = open("MACs.txt")
	time.sleep(2)
	for i in file:
		print(i)
		time.sleep(1)
		BotObj.sendMessage(chat_id=ChatID, text=i)


def TrackEm(bot, update_id):
	for update in bot.getUpdates(offset=update_id, timeout=10):
		chat_id = update.message.chat_id
		update_id = update.update_id + 1
		message = update.message.text
		if message:
			CheckAndAnswer(message, bot, chat_id)
	return update_id

def CheckForList(BotObj, ChatID):
	file = open("MACs.txt")
	for i in file:
		BotObj.sendMessage(chat_id=ChatID, text=i)


def CheckAndAnswer(Msg, BotObj, ChatID):
	MsgLowerCase = Msg.lower()
	if MsgLowerCase == "/start":
		print("/start command received")
		BotObj.sendMessage(chat_id=ChatID, text="Hey there! Would you like to scan for devices? (Type Yes, or /scan)")
		return
	if (MsgLowerCase == "yes") or (MsgLowerCase == "/scan"):
		print("/scan command received, scanning")
		BotObj.sendMessage(chat_id=ChatID, text="Ok, let's go for a quick scan!")
		time.sleep(3)
		
		print("Scan complete")
		try:
			BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n")
			print(BotObj, ChatID)
			CheckForMacs(BotObj, ChatID)
		except TypeError:
			BotObj.sendMessage(chat_id=ChatID, text="Scan complete: \n" + "No devices")

		return
	if(MsgLowerCase == "/add all"):
		BotObj.sendMessage(chat_id=ChatID, text="Ok, i'm adding everything to the list")
		time.sleep(2)
		BotObj.sendMessage(chat_id=ChatID, text=".")
		time.sleep(5)
		BotObj.sendMessage(chat_id=ChatID, text="Done!")
	if(MsgLowerCase == "/quit"):
		BotObj.sendMessage(chat_id=ChatID, text="Cya!")
	if(MsgLowerCase == "/list"):
		BotObj.sendMessage(chat_id=ChatID, text="Here is the list:")
		time.sleep(2)
		CheckForList(BotObj, ChatID)


update_id = None

BotToken = "1465290614:AAHoRrpYRmkff6aWaUNzPvpDf0611oHYmF4"

bot = telegram.Bot(BotToken)
print("TrackEm started!")

while True:
	try:
		update_id = TrackEm(bot, update_id)
	except telegram.TelegramError as e:
		if e.message in ("Bad Gateway", "Timed out"):
			sleep(1)
		else:
			raise e
