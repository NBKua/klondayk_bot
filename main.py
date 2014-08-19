#!/usr/bin/python
# coding=utf-8
from game_engine import Game
from connection import Connection
from settings import Settings
from sn import Site
import logging
import os
import errno
from user_interface import UserPrompt


logger = logging.getLogger('main')

BRANCH = 'master'

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def setup_basic_logging(gui_logger):
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.INFO, format=FORMAT,
                        stream=MyLogger(gui_logger))
    connection_logger = logging.getLogger('connection')
    connection_logger.propagate = False


def setup_file_logging(user_name, log_level):
    log_directory = 'logs/' + user_name
    mkdir_p(log_directory)
    connection_logger = logging.getLogger('connection')
    connection_logger.propagate = False
    connection_logger.addHandler(
        logging.FileHandler(log_directory + '/connection.log')
    )
    connection_logger.setLevel(log_level)
    unknownEventLogger = logging.getLogger('unknownEventLogger')
    unknownEventLogger.propagate = False
    unknownEventLogger.addHandler(
        logging.FileHandler(log_directory + '/unknown_events.log')
    )
    unknownEventLogger.setLevel(log_level)


def strip_special(string):
    return ''.join(e for e in string if e.isalnum())


def get_site(gui_input):
    settings = Settings()
    users = settings.getUsers()
    selected_user = UserPrompt(gui_input).prompt_user('Select user:', users)
    log_level = settings.get_file_log_level()
    setup_file_logging(strip_special(selected_user), log_level)
    settings.setUser(selected_user)
    site = Site(settings)
    return site, settings


def run_game(gui_input=None):
    setup_basic_logging(gui_input)

    logger.info('Выбираем пользователя...')

    site, settings = get_site(gui_input)

    Game(site, settings, UserPrompt(gui_input), gui_input=gui_input).start()


MyLogger = None

__version__ = '0.9.2 ' + BRANCH

if __name__ == '__main__':
    print '\n2013 (c) github.com/Vanuan/zombot\n version %s\n\n' % __version__
    import sys
    if 0:#len(sys.argv) != 2 or sys.argv[1] != '-c':
        import gui
        MyLogger = gui.MyLogger
        import app
        app.run_application(run_game)

    else:
        import console
        MyLogger = console.MyLogger
        run_game()
