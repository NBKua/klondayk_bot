# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class GameBuffDigger(BaseActor):
    
    def perform_action(self):
        buff_list = self._get_game_state().get_state().buffs.list
        time_digger = 0
        max_dig_time = 0
        
        for l in buff_list:
            if 'BUFF_FIX_DIGGER' in l.item:
                exp_time = float(l.expire.endDate)
                if max_dig_time < exp_time :
                    max_dig_time = exp_time

                    time_digger = (max_dig_time-self._get_timer()._get_current_client_time())/1000.0
        time_digger=int(time_digger)
        if time_digger<0: time_digger=0
        s=time_digger-int((int(time_digger/60.0)-(int(int(time_digger/60.0)/60.0)*60))*60)-int((int(int(time_digger/60.0)/60.0))*60*60)
        m=int(time_digger/60.0)-(int(int(time_digger/60.0)/60.0)*60)
        h=int(int(time_digger/60.0)/60.0)
        if time_digger>0: logger.info(u'Осталось супер-поиск: %d:%d:%d' % (h,m,s))
        else: 
            if self._get_game_state().has_in_storage("@BS_BUFF_FIX_DIGGER3", 1):
                event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"BS_BUFF_FIX_DIGGER3"}
                self._get_events_sender().send_game_events([event])
                logger.info(u"Применяю супер-поиск на 3 дня")
                buff_list.append(dict2obj({"item":"@BS_BUFF_FIX_DIGGER3", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000*3)})}))
                self._get_game_state().remove_from_storage("@BS_BUFF_FIX_DIGGER3", 1)
                
            else:
               if self._get_game_state().has_in_storage("@BS_BUFF_FIX_DIGGER2", 1):
                   event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"BS_BUFF_FIX_DIGGER2"}
                   self._get_events_sender().send_game_events([event])
                   logger.info(u"Применяю супер-поиск на 2 дня")
                   buff_list.append(dict2obj({"item":"@BS_BUFF_FIX_DIGGER2", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000*2)})}))
                   self._get_game_state().remove_from_storage("@BS_BUFF_FIX_DIGGER2", 1)
                                  
               else:
                  if self._get_game_state().has_in_storage("@BS_BUFF_FIX_DIGGER1", 1):
                      event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"BS_BUFF_FIX_DIGGER1"}
                      self._get_events_sender().send_game_events([event])
                      logger.info(u"Применяю супер-поиск на 1 день")
                      buff_list.append(dict2obj({"item":"@BS_BUFF_FIX_DIGGER1", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000)})}))
                      self._get_game_state().remove_from_storage("@BS_BUFF_FIX_DIGGER1", 1)


