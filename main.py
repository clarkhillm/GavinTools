import sip

sip.setapi('QVariant', 2)

from PyQt4 import Qt, QtCore, QtGui


class Window(QtGui.QDialog):
    def __init__(self):
        super(Window, self).__init__()

        self.quitAction = QtGui.QAction("&Quit", self, triggered=QtGui.qApp.quit)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIconMenu = QtGui.QMenu(self)
        self.trayIconMenu.addAction(self.quitAction)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QtGui.QIcon('images/heart.svg'))
        self.trayIcon.show()


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)

    if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
        QtGui.QMessageBox.critical(None, "Systray",
                                   "I couldn't detect any system tray on this system.")
        sys.exit(1)

    QtGui.QApplication.setQuitOnLastWindowClosed(False)
    window = Window()
    sys.exit(app.exec_())