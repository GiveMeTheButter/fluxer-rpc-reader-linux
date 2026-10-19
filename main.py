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


rootDir = os.path.dirname(sys.argv[0])
savedStatus = None

if sys.platform == "win32":
    raise ValueError("Windows is not currently supported")
ipcPath = str(os.environ.get("XDG_RUNTIME_DIR")) + "/" + "discord-ipc-0"
print("Path: " + ipcPath)

try:
    iconPath = os.path.join(sys._MEIPASS,"ico.svg")
except:
    iconPath = os.path.join(rootDir,"ico.svg")
tokenPath = Path(os.path.join(rootDir,"token.txt"))
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
action3 = QAction("Edit clientids.json")
def getSavedStatus():
    global savedStatus
    return savedStatus
def setSavedStatus(statuse):
    global savedStatus
    savedStatus = statuse
def exitApp():
    if(getSavedStatus() == None):
        rpcreader.setStatusNull()
    else:
        jsn = {
            "custom_status": ""
        }
        jsn["custom_status"] = getSavedStatus()
        asyncio.run(patch.setStatus(jsn))
    print("Exiting app... setting custom status to null.")
    app.quit()
def tokenWindow():
    token, done = QInputDialog.getText(dialog, "Input Token", "Input your token:")
    if(done):
        if(getSavedStatus() != None):
            jsn = {
            "custom_status": ""
            }
            jsn["custom_status"] = getSavedStatus()
            asyncio.run(patch.setStatus(jsn))
        with open(tokenPath,"r+") as tokenP:
            tokenP.seek(0)
            tokenP.write(token)
            tokenP.truncate()
        setSavedStatus(asyncio.run(patch.getStatus()))
        asyncio.run(patch.setStatusString())
def openClientids():
    subprocess.call(["xdg-open", "clientids.json"])
        
action.triggered.connect(exitApp)
action2.triggered.connect(tokenWindow)
action3.triggered.connect(openClientids)

menu = QMenu()
menu.addAction(action)
menu.addAction(action2)
menu.addAction(action3)
tray.setContextMenu(menu)

tray.show()

try:
    setSavedStatus(asyncio.run(patch.getStatus()))
    thread3 = threading.Thread(target=rpcreader.startListening, args=(ipcPath, tray,))
    thread3.daemon = True
    thread3.start()
    if(warn):
        tokenWindow()
    sys.exit(app.exec())
except KeyboardInterrupt:
    print("KeyboardInterrupt caught, setting custom status to null.")
    rpcreader.setStatusNull()