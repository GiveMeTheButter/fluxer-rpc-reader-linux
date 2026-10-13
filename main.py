import socket
import os
import json
import struct
import patch
import asyncio
import subprocess
import processjson
import sys
import timer
import threading
from pathlib import Path
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QInputDialog
from PySide6.QtGui import QIcon, QAction
import rpcreader
# add other paths later!!!

if sys.platform == "win32":
    raise ValueError("Windows is not currently supported")
ipcPath = str(os.environ.get("XDG_RUNTIME_DIR")) + "/" + "discord-ipc-0"
print("Path: " + ipcPath)

try:
    iconPath = os.path.join(sys._MEIPASS,"ico.svg")
except:
    iconPath = Path("ico.svg")
tokenPath = Path("token.txt")
warn = False
if tokenPath.exists() != True:
    print("token.txt doesn't exist! Created token.txt for you :)")
    tokenFile = open(tokenPath, "w")
    tokenFile.close()
    warn = True

app = QApplication()
dialog = QInputDialog()
QApplication.setQuitOnLastWindowClosed(False)

tray = QSystemTrayIcon()
tray.setIcon(QIcon(os.path.join(iconPath)))
tray.setToolTip("Fluxer RPC")
menu = QMenu()

action = QAction("Exit")
action2 = QAction("Change Token")

def exitApp():
    rpcreader.setStatusNull()
    print("Exiting app... setting custom status to null.")
    app.quit()
def tokenWindow():
    token, done = QInputDialog.getText(dialog, "Input Token", "Input your token:")
    if(done):
        with open(tokenPath,"r+") as tokenP:
            tokenP.seek(0)
            tokenP.write(token)
            tokenP.truncate()
        
action.triggered.connect(exitApp)
action2.triggered.connect(tokenWindow)

menu = QMenu()
menu.addAction(action)
menu.addAction(action2)
tray.setContextMenu(menu)

tray.show()

try:
    thread3 = threading.Thread(target=rpcreader.startListening, args=(ipcPath,))
    thread3.daemon = True
    thread3.start()
    if(warn):
        tokenWindow()
    sys.exit(app.exec())
    #while thread3.:
     #   thread3.start()
except KeyboardInterrupt:
    print("KeyboardInterrupt caught, setting custom status to null.")
    rpcreader.setStatusNull()