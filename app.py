import threading
from PyQt4 import QtGui
from PyQt4 import QtCore

class MyLogWindow(QtGui.QTextEdit):

    def onMessage(self, message):
        self.append(message)


class Communicate(QtCore.QObject):

    logMessage = QtCore.pyqtSignal(unicode)
    inputDialog = QtCore.pyqtSignal(unicode, list)
    onDialogDone = QtCore.pyqtSignal(unicode, bool)


class Thread(threading.Thread):

    def __init__(self, communicator, run_function):
        super(Thread, self).__init__()
        self.c = communicator
        self.run_function = run_function

    def append_log(self, message):
        self.c.logMessage.emit(message)

    def input_dialog(self, title, items):
        self.last_dialog_result = None
        self.c.inputDialog.emit(title, items)

    def run(self):
        self._running = True
        while self.running():
            self.run_function(self)

    def running(self):
       return self._running

    def on_quit(self):
       print 'quit'
       self._running = False

    def on_dialog_done(self, user_choice, done):
       self.last_dialog_result = user_choice, done

    def get_last_dialog_result(self):
       return self.last_dialog_result


class Application():

    def start_app(self, background_function):
        import sys
        app = QtGui.QApplication(sys.argv)
        self.textEdit = MyLogWindow()
        self.textEdit.showMaximized()
        self.c = Communicate()
        self.thread = Thread(self.c, background_function)

        self.c.logMessage.connect(self.textEdit.onMessage)
        self.c.inputDialog.connect(self.input_dialog)
        self.c.onDialogDone.connect(self.thread.on_dialog_done)

        app.aboutToQuit.connect(self.thread.on_quit)
        self.start_thread()
        app.exec_()

    def input_dialog(self, title, items):
        input_dialog = QtGui.QInputDialog()
        input_dialog.setComboBoxItems(items)
        input_dialog.setLabelText(title)
        input_dialog.setOptions(QtGui.QInputDialog.UseListViewForComboBoxItems)
        done = input_dialog.exec_()
        user_choice = input_dialog.textValue()
        self.c.onDialogDone.emit(user_choice, done)

    def start_thread(self):
        self.thread.start()


def run_application(background_function):
    '''
    backgound_function receives thread object
    which has append_log(message)
    '''
    t = Application()
    t.start_app(background_function)

if __name__ == '__main__':
    def run_function(logger):
       import time; time.sleep(0.1)
       logger.append_log("hohoho")

    run_application(run_function)
