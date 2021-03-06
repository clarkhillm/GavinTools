import sip
import sys


sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

from PyQt4.QtCore import Qt, SIGNAL, QThread
from PyQt4.QtGui import QBitmap, QPainter, QAction
from PyQt4 import QtGui, QtCore
import keyManager as keyM

import logging

logging.basicConfig(format='%(asctime)s -- %(message)s', level=logging.DEBUG)


class State:
    currentHotKey = ''
    currentCommand = None
    trayIconDisplayed=False


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
        self.connect(self.textEdit, SIGNAL('editTextChanged(QString)'),
                     self.text_change)

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
        self.p.drawRoundedRect(0, 0, self.width() - 1,
                               self.height() - 1, 20, 20)
        self.setMask(self.mask)

    def resizeEvent(self, event):
        self.mask_round_corner()

    def keyPressEvent(self, event):
        logging.debug('Q key id %s ', event.key())

        if event.key() == 16777216:
            self.hide()

        if event.key() == 16777220 or event.key() == 16777221:
            commnd = self.textEdit.currentText()
            logging.info('command %s', command)

            self.textEdit.setEditText('')

            if command == 'proxy':
                from commands import proxy

                proxy.execute()


class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.commandDialog = CommandDialog()

        self.exitAction = self.create_action('Q', self.close_me)

        self.test_launcher = QThread()
        self.test_launcher.run = keyM.monitor
        keyM.launcher = self.test_launcher
        keyM.launcher.connect(keyM.launcher, QtCore.SIGNAL('unhook(int)'),
                              keyM.unhook)
        keyM.launcher.connect(keyM.launcher, QtCore.SIGNAL('keyPress(QString)'),
                              self.key_press)
        self.test_launcher.start()

        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.exitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('images/heart.png'))
        self.trayIcon.activated.connect(self.on_activated)
        self.trayIcon.show()

        State.trayIconDisplayed=True

    def key_press(self, value):
        print value

    def close_me(self):
        print 'close test_launcher..'
        self.test_launcher.emit(QtCore.SIGNAL('unhook(int)'), 0)
        print 'close application..'

        self.commandDialog.close()
        self.close()
        # ctypes.windll.user32.PostQuitMessage(0)

    def create_action(self, name, handler):
        _v = QAction(name, self)
        _v.triggered.connect(handler)
        return _v

    def on_activated(self, e):
        print type(e), e
        if e == 3:
            self.commandDialog.show()
            self.commandDialog.activateWindow()
            self.commandDialog.textEdit.setFocus()
            # self.commandDialog.textEdit.clear()
            self.commandDialog.textEdit.setEditable(True)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
