import sip

sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4 import QtGui, QtCore

import pyhk


class CommandDialog(QtGui.QDialog):
    def __init__(self):
        super(CommandDialog, self).__init__()

        self.textEdit = QtGui.QLineEdit()
        self.textEdit.setMinimumWidth(500)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

        self.setWindowFlags(QtCore.Qt.Popup)


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.commandDialog = CommandDialog()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.close)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIconMenu = QtGui.QMenu(self)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('images/systray.png'))

        self.trayIcon.show()

        self.hot = pyhk.pyhk()
        # add hotkey
        self.hot.addHotkey(['Ctrl', 'Alt', 'Q'], self.close_me)
        self.hot.addHotkey(['Alt', 'Shift', '1'], self.command)
        # start looking for hotkey.
        self.hot.start()

    def close_me(self):
        self.hot.end()
        self.timer.start(10)

    def command(self):
        if not self.commandDialog.isVisible():
            self.commandDialog.show()
            #self.commandDialog.activateWindow()
            self.commandDialog.textEdit.setFocus()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, 'Systray',
                                   'I couldn\'t detect any system tray on this system.')
        sys.exit(1)

    window = Window()
    sys.exit(app.exec_())
