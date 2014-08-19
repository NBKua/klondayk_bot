import sys
from PyQt4 import QtGui
import logging

class MyLogger(logging.StreamHandler):

    def __init__(self, gui_logger):
        super(MyLogger, self).__init__()
        self.gui_logger = gui_logger

    def write(self, message):
        self.gui_logger.append_log(message.decode('utf-8').strip('\n'))


class InputClass(object):

    def __init__(self, gui_input):
        self.gui_input = gui_input

    def raw_input(self, prompt):
        prompt = prompt.decode('utf-8')

        title = prompt.split('\n')[0].split(':')[0]
        items = filter(None, prompt.split('\n')[1:])

        self.gui_input.input_dialog(title, items)
        while not self.gui_input.get_last_dialog_result():
            pass
        user_choice, done = self.gui_input.get_last_dialog_result()

        if not done:
            sys.exit(-1)
        return items.index(unicode(user_choice)) + 1
