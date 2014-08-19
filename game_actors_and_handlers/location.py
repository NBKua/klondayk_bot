# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
import collections

logger = logging.getLogger(__name__)


class ChangeLocationBot(BaseActor):
    '''
    Changes location

    @param options: Available receive options:

    selected_location: location to change to
    '''

    def perform_action(self):
        loc_setting = self._get_options()
        self.__init_visit_queue(loc_setting)
        next_loc_id = self.__get_next_loc_id(loc_setting)
        self.__change_location(next_loc_id)

    def __init_visit_queue(self,loc_setting):
        #{'locations_only':'[u"isle_polar"]','locations_nfree = [u"isle_01", u"isle_small", u"isle_star", u"isle_large", u"isle_moon", u"isle_giant", u"isle_xxl", u"isle_desert"]','locations_nwalk':'[u"un_0"+str(x+1) for x in range(9)]','locations_nother':'[]'}
        
        if not hasattr(self, '_visit_queue'):
            self._visit_queue = collections.deque()
            # Только определенные локации
            locations_only=eval(loc_setting['locations_only'])
            if (locations_only==[]):
                # Запрет платных островов
                locations_nfree = eval(loc_setting['locations_nfree'])
                # Запрет пещер
                locations_nwalk = eval(loc_setting['locations_nwalk'])
                # Прочие запреты
                locations_nother = eval(loc_setting['locations_nother'])
                for location in self._get_game_state().get_state().locationInfos:
                    if (location.locationId not in locations_nfree) and (location.locationId not in locations_nwalk) and (location.locationId not in locations_nother):
                        self._visit_queue.appendleft(location.locationId)
            else:
                self._visit_queue = collections.deque(locations_only)
                

    def __change_location(self, location_id):
        logger.info(u'Переходим на ' + self.__get_location_name(location_id))
        change_location_event = {
          "user": None,
          "locationId" : location_id,
          "type":"gameState",
          "action":"gameState",
          "objId": None
        }
        self._get_events_sender().send_game_events([change_location_event])

    def __get_location_name(self, location_id):
        name = self._get_item_reader().get(location_id).name
        return name

    def __get_next_loc_id(self,loc_setting):
        locations_only=eval(loc_setting['locations_only'])
        if (locations_only==[]):
            # Запрет платных островов
            locations_nfree = eval(loc_setting['locations_nfree'])
            # Запрет пещер
            locations_nwalk = eval(loc_setting['locations_nwalk'])
            # Прочие запреты
            locations_nother = eval(loc_setting['locations_nother'])
            current_loc_id = self._get_game_state().get_location_id()
            if (current_loc_id not in locations_nfree) and (current_loc_id not in locations_nwalk) and (current_loc_id not in locations_nother):
                self._visit_queue.appendleft(current_loc_id)
        else:
            current_loc_id = self._get_game_state().get_location_id()
            if current_loc_id in locations_only:
                self._visit_queue.appendleft(current_loc_id)
        next_loc_id = self._visit_queue.pop()
        return next_loc_id


class GameStateEventHandler(object):
    def __init__(self, game_state, timer,setting_view):
        self.__game_state = game_state
        self.__timer = timer
        self.__setting_view = setting_view

    def handle(self, event_to_handle):
        if event_to_handle is None:
            logger.critical("OMG! No such object")
            return
        else:
            if self.__setting_view['location_send']:
                if (hasattr(event_to_handle, "locationId") is True ): logger.info(u'Перешли на ' + event_to_handle.locationId)
            if 0: 
                info_guest=event_to_handle.location.guestInfos
                logger.info(u'Гости:')
                for guest in info_guest:
                    jet = self.__timer - guest.visitingTime
                    s = (jet/1000)-(((jet/1000)/60)*60)
                    m = ((jet/1000)/60)-((((jet/1000)/60)/60)*60)
                    h = ((jet/1000)/60)/60
                    logger.info(u'%s\tбыл в %d:%d:%d\tник "%s"'%(guest.userId,h,m,s,guest.playerSettings.userName))
            self.__game_state.set_game_loc(event_to_handle)
