import logging

from PyQt4 import QtCore
from PyQt4.QtCore import QThread

from doProxy import proxy

test = QThread()


def update(info):
    logging.info('message: %s', info)


test.run = proxy.main(test)
test.connect(test, QtCore.SIGNAL('update(QString)'), update)


def execute():
    logging.info('start thread..')
    test.start()