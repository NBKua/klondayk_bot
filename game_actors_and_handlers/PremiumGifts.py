# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameApplyGiftEvent, GameGift
from game_state.game_event import dict2obj, obj2dict
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup
from game_actors_and_handlers.base import BaseActor
#from ctypes import windll
import sys
import time

logger = logging.getLogger(__name__)

class PremiumGifts(BaseActor):
    
    def perform_action(self):

        location_id = "main"
        #specified_gift = '@VALENT_GIFT_BOX6'  # зомбилетто
        rezhim = 2  # режим: 1 - покупать, 2 - принимать
        count = 500  # сколько за раз
        specified_gift = '@MARCH_GIFT_BOX1'  # корзина мимоз rezhim 1
        specified_gifts = ['@MARCH_GIFT_BOX1', '@VALENT_GIFT_BOX6' ,'@BIRTHDAY_GIFT_BOX1','@BIRTHDAY_GIFT_BOX2','@BIRTHDAY_GIFT_BOX3','@BIRTHDAY_GIFT_BOX4','@BIRTHDAY_GIFT_BOX5','@BIRTHDAY_GIFT_BOX6','@BIRTHDAY_GIFT_BOX7', '@B_PAINTBALL_TARGET1']  # rezhim 2
        free_x = 25  # Координаты пустого места
        free_y = 52
        min_money = 10000000  # оставляем денег
        
        location = self._get_game_state().get_game_loc().get_location_id()
        #print location
        if location == location_id:
            next_id = max([_i.maxGameObjectId for _i in self._get_game_state().get_state().locationInfos] +[_m.id for _m in self._get_game_location().get_game_objects()])
            if rezhim == 1:
                build_cost = self._get_item_reader().get(specified_gift[1:]).buyCoins
                if self._get_game_state().get_state().gameMoney > min_money:
                    num = 0
                    for _ in range(count):  
                        if self._get_game_state().get_state().gameMoney > min_money:
                            num += 1
                            next_id = next_id + 1
                            buy_gift = {"x":free_x,"action":"buy","y":free_y,"itemId":specified_gift[1:],"type":"item","objId":next_id}
                            print u'Покупаем подарок ', _
                            self._get_events_sender().send_game_events([buy_gift])
                            #print u'Открываем подарок'
                            open_event={"action":"pick","type":"item","objId":next_id}
                            self._get_events_sender().send_game_events([open_event])
                            self._get_game_state().get_state().gameMoney -= build_cost
                    logger.info(u"  ------------------------------------  ")
                    logger.info(u"Купили и вскрыли "+str(num)+u" шт. "+specified_gift)
                    logger.info(u"  ------------------------------------  ")
            else:
                gifts = list(set(self._get_game_state().get_state().gifts))
                for gift in gifts:
                    num = 0
                    print gift.item
                    if gift.item in specified_gifts:
                        for co in range(gift.count):                    
                            next_id = next_id + 1 
#"events":[{"x":84,"extraId":931,"y":74,"objId":182,"type":"item","itemId":"VALENT_GIFT_BOX6","action":"applyCompGift"}]
                            apply_event={
                                "x":free_x, 
                                "y":free_y,
                                "extraId":gift.id,
                                "action":"applyCompGift",
                                "itemId":gift.item[1:],
                                "type":"item",
                                "objId":next_id 
                                }
                            print u'Устанавливаем подарок ', co 
                            self._get_events_sender().send_game_events([apply_event])
                            #print u'Открываем подарок'
                            open_event={"action":"pick","type":"item","objId":next_id}
                            self._get_events_sender().send_game_events([open_event])
                            num += 1
                            #time.sleep(0.003)
                            if not num % 500:
                                time.sleep(2)
                                break
                        if num >= count:
                            break
                        self._get_game_state().get_state().gifts.remove(gift)
                    if num > 0:
                        logger.info(u"  ------------------------------------  ")
                        logger.info(u"Приняли и вскрыли "+str(num)+u" шт. "+gift.item[1:])
                        logger.info(u"  ------------------------------------  ")

'''
#min_money = 1000000000  # оставляем денег
ставим:
{"events":[{"objId":14918,"x":99,"y":4,"extraId":204061,"type":"item","itemId":"VALENT_GIFT_BOX6","action":"applyCompGift"}]}
{"events":[{"objId":14919,"x":96,"y":5,"extraId":203891,"type":"item","itemId":"VALENT_GIFT_BOX6","action":"applyCompGift"}]}

            
вскрываем:
{"events":[{"objId":14918,"type":"item","action":"pick"}]}
покупаем
{"events":[{"objId":14920,"x":96,"y":6,"action":"buy","type":"item","itemId":"VALENT_GIFT_BOX6"}]}            
'''