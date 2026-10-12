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
from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtGui import QIcon, QAction
import rpcreader
# add other paths later!!!

if sys.platform == "win32":
    raise ValueError("Windows is not currently supported")
ipcPath = str(os.environ.get("XDG_RUNTIME_DIR")) + "/" + "discord-ipc-0"
print("Path: " + ipcPath)

app = QApplication()
QApplication.setQuitOnLastWindowClosed(False)

tray = QSystemTrayIcon()
tray.setIcon(QIcon("saul.jpg"))
menu = QMenu()

tray.show()

action = QAction("Exit")

def exitApp():
    rpcreader.setStatusNull()
    print("Exiting app... setting custom status to null.")
    app.quit()
action.triggered.connect(exitApp)

menu = QMenu()
menu.addAction(action)
tray.setContextMenu(menu)

tray.show()

try:
    thread3 = threading.Thread(target=rpcreader.startListening, args=(ipcPath,))
    thread3.daemon = True
    thread3.start()
    sys.exit(app.exec())
    #while thread3.:
     #   thread3.start()
except KeyboardInterrupt:
    print("KeyboardInterrupt caught, setting custom status to null.")
    rpcreader.setStatusNull()