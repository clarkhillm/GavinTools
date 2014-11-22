import logging

from PyQt4 import QtCore

from PyQt4.QtCore import QThread

from doProxy import proxy

test = QThread()


def work():
    proxy.main(test)


def update(info):
    logging.info('message: %s', info)


test.run = work
test.connect(test, QtCore.SIGNAL('update(QString)'), update)


def execute():
    logging.info('start thread..')
    test.start()