import sip
import sys

sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QBitmap, QPainter
from PyQt4 import QtGui, QtCore

import pyhk


class CommandDialog(QtGui.QDialog):
    def __init__(self):
        super(CommandDialog, self).__init__()

        self.mask = None
        self.p = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.textEdit = QtGui.QLineEdit()
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.textEdit.setMinimumWidth(500)
        self.textEdit.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 4px;")

    def mask_round_corner(self):
        self.mask = QBitmap(self.size())
        self.mask.clear()
        self.p = QPainter(self.mask)
        self.p.fillRect(self.rect(), Qt.white)
        self.p.setBrush(Qt.black)
        self.p.drawRoundedRect(0, 0, self.width() - 1, self.height() - 1, 20, 20)
        self.setMask(self.mask)

    def resizeEvent(self, event):
        self.mask_round_corner()


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.commandDialog = CommandDialog()

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIconMenu = QtGui.QMenu(self)

        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('images/systray.png'))

        self.trayIcon.show()

        self.hot = pyhk.pyhk()
        # add hotkey
        self.hot.addHotkey(['Ctrl', 'Alt', 'Q'], self.close_me)
        self.hot.addHotkey(['Alt', 'Shift', 'C'], self.command)
        # start looking for hotkey.
        self.hot.start()

    @staticmethod
    def close_me():
        sys.exit(1)

    def command(self):
        if not self.commandDialog.isVisible():
            self.commandDialog.show()
            self.commandDialog.activateWindow()
            self.commandDialog.textEdit.setFocus()
            self.commandDialog.textEdit.clear()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
