# coding=utf-8
import logging
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameCollectionItems
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup, GameUseStorageItem
from game_state.item_reader import LogicalItemReader

logger = logging.getLogger(__name__)

class Exchange_Collection(BaseActor):
    def perform_action(self):
        count = 1 #сколько менять
        itemId = 'C_2' #C_1,C_2 = номер коллекции

        coll=obj2dict(self._get_game_state().get_state().collectionItems)
        max_coll = [int(coll[itemId+'_'+str(_i)]) for _i in range(1,6) if (itemId+'_'+str(_i) in coll.keys())]
        if len(max_coll) == 5 and min(max_coll)>=count:
            #меняем коллекции
            col_exchange = {"count":count,
                            "itemId":itemId,
                            "action":"collect",
                            "type":"item"} 
            self._get_events_sender().send_game_events([col_exchange])
            logger.info(u'Обмениваем '+str(self._get_item_reader().get('@'+itemId).name) + ' ' + str(count)+u' раз')
        else:
            logger.info(u'Не хватает чего-то для обмена')
