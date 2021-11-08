"""
Full module list obtained from: http://timgolden.me.uk/pywin32-docs/win32_modules.html

Skipped modules:

_winxptheme: private module
wincerapi: interface to the win32 CE Remote API
"""
import mmapfile
import odbc
import perfmon
import pywintypes
import servicemanager
import timer
import win2kras
import win32api
import win32clipboard
import win32console
import win32cred
import win32crypt
import win32event
import win32evtlog
import win32file
import win32gui
import win32help
import win32inet
import win32job
import win32lz
import win32net
import win32pdh
import win32pipe
import win32print
import win32process
import win32profile
import win32ras
import win32security
import win32service
import win32transaction
import win32ts
import win32wnet

import os

conda_py = str(os.sys.version_info.major) + str(os.sys.version_info.minor)

pythoncom_filename = os.environ["LIBRARY_BIN"] + "\pythoncom" + conda_py + ".dll"
pywintypes_filename = os.environ["LIBRARY_BIN"] + "\pywintypes" + conda_py + ".dll"

assert os.path.isfile(pythoncom_filename)
assert os.path.isfile(pywintypes_filename)
