# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class GameBuffDigger(BaseActor):
    
    def perform_action(self):
        is_there_digger_buff = False
        buff_list = self._get_game_state().get_state().buffs.list
        for buff in buff_list:
            if buff.item == "@BS_BUFF_FIX_DIGGER1":
                time_exp = buff.expire.endDate
                is_there_digger_buff = True
        if is_there_digger_buff == False or self._get_timer().has_elapsed(time_exp):
            if self._get_game_state().has_in_storage("@BS_BUFF_FIX_DIGGER1", 1):
                event = {"x":20,"type":"item","y":7,"action":"useStorageItem","itemId":"@BS_BUFF_FIX_DIGGER1"}
                self._get_events_sender().send_game_events([event])
                logger.info(u"Применяю супер-поиск на 1 день")
                buff_list.append(dict2obj({"item":"@BS_BUFF_FIX_DIGGER1", "expire": dict2obj({"type":"time", "endDate": str(int(self._get_timer()._get_current_client_time())+86400000)})}))
                self._get_game_state().remove_from_storage("@BS_BUFF_FIX_DIGGER1", 1)