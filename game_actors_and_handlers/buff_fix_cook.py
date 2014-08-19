# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class GameBuffFixCook(BaseActor):
    
    def perform_action(self):

        max_harv_time = 0
        for l in self._get_game_state().get_state().buffs.list:
            if 'BUFF_FIX_COOK' in l.item:      #BUFF_FIX_COOK_1
                exp_time = float(l.expire.endDate)
                if max_harv_time < exp_time :
                    max_harv_time = exp_time

        time_harvest = (max_harv_time-self._get_timer()._get_current_client_time())/1000.0
        time_harvest=int(time_harvest)
        if time_harvest<0: time_harvest=0
        s=time_harvest-int((int(time_harvest/60.0)-(int(int(time_harvest/60.0)/60.0)*60))*60)-int((int(int(time_harvest/60.0)/60.0))*60*60)
        m=int(time_harvest/60.0)-(int(int(time_harvest/60.0)/60.0)*60)
        h=int(int(time_harvest/60.0)/60.0)
        if time_harvest<>0: logger.info(u'Осталось минутки-на-день: %d:%d:%d' % (h,m,s))

        is_there_harvest_buff = False
        buff_list = self._get_game_state().get_state().buffs.list
        for buff in buff_list:
            if buff.item == "@BUFF_FIX_COOK_1":
                time_exp = buff.expire.endDate
                is_there_harvest_buff = True
        if is_there_harvest_buff == False or self._get_timer().has_elapsed(time_exp) or time_harvest<30: 
            if self._get_game_state().has_in_storage("@BS_BUFF_FIX_COOK_1", 1):
                event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"BS_BUFF_FIX_COOK_1"}
                self._get_events_sender().send_game_events([event])
                logger.info(u"Применяю минутки-на-день на 24 часа")
                buff_list.append(dict2obj({"item":"@BUFF_FIX_COOK_1", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000)})}))
                self._get_game_state().remove_from_storage("@BUFF_FIX_COOK_1", 1)