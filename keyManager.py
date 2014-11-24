import ctypes

from PyQt4 import QtCore
import pyHook
import pythoncom

__author__ = 'gavin'


def monitor(launcher):
    print 'launcher', launcher

    def on_key_down(event):
        if event.Ascii > 0:
            print ('Ascii: %s (%s) ,Key %s (%s)'
                   % (chr(event.Ascii), event.Ascii, event.Key, event.KeyID))

    hm = pyHook.HookManager()
    hm.KeyDown = on_key_down
    hm.HookKeyboard()

    def unhook(a):
        print 'unhook', a
        hm.UnhookKeyboard()
        ctypes.windll.user32.PostQuitMessage(0)
        launcher.quit()

    launcher.connect(launcher, QtCore.SIGNAL('unhook(int)'), unhook)

    pythoncom.PumpMessages()
