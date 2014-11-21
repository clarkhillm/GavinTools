from PyQt4.QtCore import QThread

__author__ = 'cwx205128'

from doProxy import proxy


class ProxyServer(QThread):
    def run(self):
        proxy.main()


def execute():
    ProxyServer().start()