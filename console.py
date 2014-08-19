import logging

class MyLogger(logging.StreamHandler):

    def __init__(self, gui_logger):
        super(MyLogger, self).__init__()
        self.gui_logger = gui_logger

    def write(self, message):
      print message.decode('utf-8'),

