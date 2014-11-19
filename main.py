import sip

sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore

import pyhk


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.quitAction = QtGui.QAction("&Quit", self, triggered=self.close_me)
        self.testAction = QtGui.QAction('Test', self, triggered=self.test)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.close)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIconMenu.addAction(self.testAction)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('images/heart.svg'))

        self.trayIcon.show()

        self.hot = pyhk.pyhk()
        # add hotkey
        self.hot.addHotkey(['Ctrl', 'Alt', 'Q'], self.fun)
        # start looking for hotkey.
        self.hot.start()

    def close_me(self):
        self.hot.end()
        self.timer.start(100)

    def test(self):
        print('test')

    def fun(self):
        self.test()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, 'Systray',
                                   'I couldn\'t detect any system tray on this system.')
        sys.exit(1)

    window = Window()
    sys.exit(app.exec_())
