import sip
import sys

sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QBitmap, QPainter
from PyQt4 import QtGui, QtCore

import pyhk


class State:
    currentHotKey = ''
    currentCommand = None

    def __init__(self):
        pass


class CommandDialog(QtGui.QDialog):
    def __init__(self):
        super(CommandDialog, self).__init__()

        self.setFocusPolicy(Qt.TabFocus)

        self.mask = None
        self.p = None

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.textEdit = QtGui.QComboBox(self)
        # self.textEdit.addItem("")
        self.textEdit.setMinimumWidth(500)
        self.textEdit.setStyleSheet(
            """
            QComboBox {
                 border:2px groove gray;
                 border-radius:10px;
                 padding:2px 4px;
             }
             QComboBox::drop-down {
                border:0px;
                left:100px;
             }
             """)
        self.textEdit.setAutoCompletion(True)
        self.connect(self.textEdit, SIGNAL('editTextChanged(QString)'), self.text_change)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textEdit)
        self.setLayout(layout)

    def text_change(self, value):
        if State.currentHotKey == 'command' and value == 'C':
            self.textEdit.setEditText(value.rstrip('C'))

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

    def keyPressEvent(self, event):
        if event.key() == 16777220 or event.key == 16777221:
            command = self.textEdit.currentText()
            self.textEdit.setEditText('')

            if command == 'proxy':
                from commands import proxy

                proxy.execute()


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
        self.hot.addHotkey(['Ctrl', 'Alt', 'C'], self.command)
        # start looking for hotkey.
        self.hot.start()

    @staticmethod
    def close_me():
        sys.exit(1)

    def command(self):
        State.currentHotKey = 'command'

        if not self.commandDialog.isVisible():
            self.commandDialog.show()
            self.commandDialog.activateWindow()
            self.commandDialog.textEdit.setFocus()
            # self.commandDialog.textEdit.clear()
            self.commandDialog.textEdit.setEditable(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
