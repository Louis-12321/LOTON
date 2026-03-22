import sys
import time
import os
import random
os.system("title Loton OS v1.0.0.0")
# Variables
Text = "Loton [Version 1.0.0.0]"
sleeptime = 0.05

# Typewriter effect
def typewritter(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sleeptime)
    print("")

# Initial messages
os.system("cls" if os.name == "nt" else "clear")
typewritter(Text)
Text = "Loton Corporation. All rights reserved."
typewritter(Text)

# Main loop
while True:
    sys.stdout.write("#L:|Accounts|ADMIN > ")
    action = input().strip()

    if action == "/exit":
        Text = "Exiting LOTON..."
        typewritter(Text)
        time.sleep(1)
        sys.exit()

    elif action == "/help":
        Text = ("Commands: /help, /exit, /clear, /info, /ver, /systeminfo, "
                "/echo, /ping, /password, /user.")
        typewritter(Text)

    elif action == "/clear":
        os.system("cls" if os.name == "nt" else "clear")

    elif action == "/info":
        Text = "LOTON Corporation © , All Rights Reserved."
        typewritter(Text)
        Text = "Found date: 2025"
        typewritter(Text)
        Text = "Current version: 1.0.0.1"
        typewritter(Text)
        Text = "Current Loton: Loton 1"
        typewritter(Text)
        Text = "Current New versions: None"
        typewritter(Text)

    elif action == "/ver":
        Text = "Current Version: 1.0.0.0"
        typewritter(Text)
        Text= "[Loton 1]"
        typewritter(Text)
        Text = "Update available: LOTON 1.1.0.0"
        typewritter(Text)
    
    elif action == "/systeminfo":
        Text = "System name: Loton 1"
        typewritter(Text)
        Text = "Available versions: 1.0.0.0"
        typewritter(Text)

    elif action.startswith("/echo"):
        message = action[6:] if len(action) > 5 else ""
        typewritter(message)

    elif action == "/ping Google.com" or action == "/ping internet" or action == "/ping Internet" or action == "/ping LotonCorp.com":
        Text = "Pinging...                                                                "
        typewritter(Text)
        internet = random.randint(1, 10)
        if internet % 2 == 0 or internet % 2 == 1:
            Text = "Ping successful"
            typewritter(Text)
            Text = "Connected to Internet"
            typewritter(Text)
        else:
            Text = "Ping unsuccessful"
            typewritter(Text)
            Text = "Not connected to Internet"
            typewritter(Text)

    elif action == "/password":
        passtrue = random.randint(1, 10)
        if passtrue != 0:
            Text = "Password (unshown): *******"
            typewritter(Text)
        else:
            Text = "Password not set"
            typewritter(Text)

    elif action == "/user":
        Text = "Current Username: USER"
        typewritter(Text)
        Text = "If you want to change username, please contact us: "
        typewritter(Text)
        Text = "Loton Corporation email: lotoncorp@2026.com"
        typewritter(Text)
        Text = "Founder email: hailouis2013@gmail.com"
        typewritter(Text)

    else:
        Text = "Command not found:" + str(action)
        typewritter(Text)
