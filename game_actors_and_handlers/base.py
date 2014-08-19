import sys
import re


class BaseActor(object):
    def __init__(self, item_reader, game_state,
                  events_sender, timer, options):
        self.__item_reader = item_reader
        self.__game_state = game_state
        self.__events_sender = events_sender
        if self.__class__.__name__ in options:
            self.__options = options[self.__class__.__name__]
        self.__timer = timer

    def _get_options(self):
        return self.__options

    def _get_item_reader(self):
        return self.__item_reader

    def _get_game_state(self):
        return self.__game_state

    def _get_events_sender(self):
        return self.__events_sender

    def _get_timer(self):
        return self.__timer

    def _get_game_location(self):
        location = self._get_game_state().get_game_loc()
        return location

    def _get_player_brains(self):
        return self._get_game_state().get_brains()
