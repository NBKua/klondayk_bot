# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameTraderGraveWithBrains, GameTraderGrave
from game_state.game_event import obj2dict
logger = logging.getLogger(__name__)


class TraderWork(BaseActor):

    def get_worker_types(self):
        return [GameTraderGrave.type, GameTraderGraveWithBrains.type]

    def perform_action(self):
        #graves = self._get_game_location().get_all_objects_by_types(self.get_worker_types())
        loc_obj = self._get_game_location().get_all_objects_by_types(self.get_worker_types())
        for _obj in loc_obj:
            if "SC_TRADER_GRAVE" in _obj.item:
                #print _obj.item
                #print _obj.x + _obj.y
                #print getattr(obj2dict(_obj.give), 'item')
                #print obj2dict(_obj.give) + obj2dict(_obj.want)
                if _obj.started == False:
                    trader_event = {"objId":_obj.id,
                                    "type":"item",
                                    "action":"start"}
                    self._get_events_sender().send_game_events([trader_event])
                      #print u'Выгоняем на работу торгаша № ',_obj.id
                    logger.info("Отправляем работаеть торговца №%s",_obj.id)
                    _obj.started = True

                if _obj.countCompleted == 1:
                    trader_event = {"objId":_obj.id,
                                    "type":"item",
                                    "action":"pick"}
                    self._get_events_sender().send_game_events([trader_event])
                    #print u'Забираем коробку у торгаша № ',_obj.id
                    logger.info("Забираем коробку у торговца №%s",_obj.id)
                    print obj2dict(_obj.give) + obj2dict(_obj.want)
                    open('trader.txt','a').write(str(obj2dict(_obj.give)) + str(obj2dict(_obj.want)) + "\n")
                    _obj.countCompleted = 0

                if _obj.countExchange == 0 and _obj.countCompleted == 0:
                    trader_event = {"objId":_obj.id,
                                    "type":"trader",
                                    "want":_obj.want,
                                    "give":_obj.give,
                                    "action":"change",
                                    "countExchange":1}
                    self._get_events_sender().send_game_events([trader_event])
                    logger.info("Обновляем торговца №%s",_obj.id)
                    _obj.countExchange = 1


