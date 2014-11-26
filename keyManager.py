from PyQt4 import QtCore

import pyHook
import pythoncom

__author__ = 'gavin'

launcher = None


def on_key_down(event):
    # print ('Ascii: %s (%s) ,Key %s (%s)'
    # % (chr(event.Ascii), event.Ascii, event.Key, event.KeyID))
    launcher.emit(QtCore.SIGNAL('keyPress(QString)'),
                  str(event.Ascii) + ',' + event.Key + ',' + str(event.KeyID))


hm = pyHook.HookManager()
hm.KeyDown = on_key_down
hm.HookKeyboard()


def unhook(a):
    print 'unhook', a
    hm.UnhookKeyboard()
    launcher.terminate()


def monitor():
    pythoncom.PumpMessages()
