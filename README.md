## SWRATT
 A simple Windows Remote Administration Tool using Telegram bot function.

## Features:

- Show current directory
- Change current directory
- List current or specified directory
- Download file from the target
- Screenshots
- Execute file
- Execute cmd

## Screenshots:

<img src="https://i.imgur.com/B8Kcpv0.png"/>

## Installation & Usage:

- Clone this repository: `git clone https://github.com/Suburbanno/SWRATT.git`
- Set up a new Telegram bot talking to the `@BotFather`.
- Copy this token and replace it in `token = "xxxxxxxxxxxxxxx"`.
- Run `main.py`
  - Copy your `chat_id` from the console and replace it in `trusted_users = [xxxxx]` and group id in `trusted_chats = [-xxxxx]`if you need.
  - You have the option to get your id and the group id through this `@my_id_bot` bot, for that you must put the bot in a group exists or create a test group
  <img src="https://i.imgur.com/579fkJG.jpg"/>
- Go to your bot on telegram and send `/help` command to the bot to test it.

### Commands:

```
/screen - screenshot PC
/cd - change current directory
/download - download file from target
/ls - list contents of current or specified directory
/pwd - show current directory
/run - run a file
/cmd - execute cmd
```

## Compiling:

### How To Compile:
`pyinstaller --icon YOUR_ICON --noconsole -F main.py`

---
- `--icon YOUR_ICON` Uses the icon in the format .ICO
- `--noconsole` Does not show the console while the program is running
- `-F` Compiles the file in .exe

## Contributing:
Contributions and feature requests are welcome!<br />Feel free to open a [issue](https://github.com/Suburbanno/SWRATT/issues) or [pull request](https://github.com/Suburbanno/SWRATT/pulls).

## Disclaimer:

**This tool should be used only for studies or in controlled environments under authorization, otherwise it is illegal..**

## License:

[The MIT License](https://github.com/Suburbanno/SWRATT/blob/master/LICENSE)
