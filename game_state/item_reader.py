from game_state.game_event import dict2obj
import json
import logging
import os
import time
from connection import Connection
import pprint
from settings import Settings


class MyPrettyPrinter(pprint.PrettyPrinter):
    def format(self, obj, context, maxlevels, level):
        if isinstance(obj, unicode):
            return (obj.encode('utf8'), True, False)
        return pprint.PrettyPrinter.format(self, obj,
                                           context, maxlevels, level)


class GameItemReader():
    def __init__(self):
        self.content_dict = {}
        settings = Settings()
        self.__ignore_errors = settings.get_ignore_errors()

    def get(self, item_id):
        item_id = str(item_id).lstrip('@')
        return dict2obj(self.content_dict[item_id])

    def get_name(self, item):
        return self.get(item.item).name

    def read(self, filename):
        with open(filename) as f:
            self.contents = json.load(f)
        for content in self.contents:
            if 'id' not in content:
                logging.debug(u"there is no id: %s" % content)
            else:
                self.content_dict[content['id']] = content

    def _getModificationTime(self, filename):
        try:
            return time.localtime(os.path.getmtime(filename))
        except OSError:  # no such file
            return None

    def download(self, filename):
        last_modified_time = self._getModificationTime(filename)
        #url = 'http://jok.shadowlands.ru/zombieok/items'
        #url = 'http://java.shadowlands.ru/zombievk/items' 
        #url = 'http://jmr.shadowlands.ru/zombiemr/items'
        url = 'http://klone-mr.shadowlands.ru/klonemr/items'
        if not self.__ignore_errors:
          data = Connection(url).getChangedDocument(
              data={'lang': 'ru'},
              last_client_time=last_modified_time
              )
        else:
          while 1:
              try:
                  print 'Download items...'
                  data = Connection(url).getChangedDocument(
                      data={'lang': 'ru'},
                      last_client_time=last_modified_time
                  )
                  print 'Items downloaded!'
                  break
              except: print 'Refresh download...'
        with open(filename, 'w') as f:
            f.write(data.encode('utf-8'))

    def pretty_write(self, filename):
        with open(filename, 'w') as f:
            pretty_dict = MyPrettyPrinter().pformat(self.content_dict)
            f.write(pretty_dict)



class LogicalItemReader(object):
    'defines item ids and names that are available to use'

    def __init__(self, game_item_reader):
        self._item_reader = game_item_reader

    def get_avail_names(self, game_state):
        return sorted(self.__get_items_available(game_state).keys())

    def get_by_name(self, item_name):
        items = self.__get_name_to_item()
        if item_name in items:
            return items[item_name]

    def is_item_available(self, item, game_state):
        level = game_state.get_state().level
        location_id = game_state.get_game_loc().get_location_id()
        location = self._item_reader.get(location_id)
        allowed_here = (not hasattr(location, 'allowCompositionIds') or \
                        item.id in location.allowCompositionIds) and \
                       (not hasattr(item, 'locations') or \
                        location_id in item.locations)
        is_a_type = item.type == self._get_item_type()
        allowed_for_level = not hasattr(item, 'level') or item.level <= level
        return is_a_type and allowed_here and allowed_for_level

    def __get_name_to_item(self):
        items = {}
        item_ids = self._get_all_item_ids()
        for item_id in item_ids:
            item = self._item_reader.get(item_id)
            items[item.name] = item
        return items

    def __get_items_available(self, game_state):
        items = self.__get_name_to_item()
        items = {k: v for k, v in items.iteritems()\
                      if self.is_item_available(v, game_state)}
        return items

    def _get_all_item_ids(self):
        raise NotImplementedError  # inherit and implement

    def _get_item_type(self):
        raise NotImplementedError  # inherit and implement
