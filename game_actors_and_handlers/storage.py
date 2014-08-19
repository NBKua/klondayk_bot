# coding=utf-8
import logging
from game_state.game_types import GameSellItem, GameSendGift
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict

logger = logging.getLogger(__name__)

class SellBot(BaseActor):

    def perform_action(self):
        # Продажа
        sell_items = self._get_options()['sell_item']
        if sell_items<>None:
            #sell_items={u'S_51':20}
            #item_id=u'S_51' # Красные яблоки
            #item_save_count=20
            for item_id in sell_items.keys():
                item_save_count=sell_items[item_id]
                itm_count=self._get_game_state().count_in_storage('@'+item_id)
                item_count=itm_count-item_save_count
                if item_count>0:
                    sell_event = GameSellItem(count=long(item_count), itemId = unicode(item_id))
                    self._get_events_sender().send_game_events([sell_event])
                    self._get_game_state().remove_from_storage('@'+item_id,item_count)
                    itm_count=self._get_game_state().count_in_storage('@'+item_id)
                    logger.info(u"Продали %d '%s' осталось %d"%((item_count),self._get_item_reader().get(item_id).name,itm_count))
                    
        CollIt=obj2dict(self._get_game_state().get_state().collectionItems)
        send_user = self._get_options()['send_user']
        # "26586292"
        if send_user<>None:
            for item_id in CollIt.keys():
                #print item_id+'\t-\t'+str(CollIt[item_id])
                #{"gift":{"item":"@CR_53","msg":"","count":1,"user":"176312587"},"action":"sendGift","id":55,"type":"gift"}
                #{"gift":{"msg":"","item":"C_4_1","count":1,"user":"26586292"},"action":"sendGift","type":"gift"}
                if CollIt[item_id]>0:
                    send_gift={
                        "item":'@'+item_id,
                        "msg":"",
                        "count":CollIt[item_id],
                        "user":send_user
                        }
                    event=GameSendGift(gift=send_gift)
                    self._get_events_sender().send_game_events([event])
                    #print 'Otpravleno\t'+str(CollIt[item_id])+'\t'+item_id
                    logger.info(u"Отправили %d '%s' пользователю %d"%(CollIt[item_id],self._get_item_reader().get(item_id).name,int(send_user)))
                    self._get_game_state().remove_from_storage('@'+item_id, CollIt[item_id])
                    CollIt[item_id]=0
        self._get_game_state().get_state().collectionItems=dict2obj(CollIt)