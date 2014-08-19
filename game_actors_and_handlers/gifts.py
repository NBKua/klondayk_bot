# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameApplyGiftEvent, GameGift
logger = logging.getLogger(__name__)


class GiftReceiverBot(BaseActor):
    '''
    Receives gifts

    @param options: Available receive options:

    with_messages: receive gifts with messages
    non_free: receive non-free gifts
    '''

    def perform_action(self):
        self.receive_all_gifts()

    def receive_all_gifts(self):
        gifts = self._get_game_state().get_state().gifts
        # print dir(gifts[0])
        #[ u'count', u'free', u'id', u'item', u'msg', u'type', u'user']
        if len(gifts) > 0:
            logger.info(u"Доступно подарков: %s" % len(gifts))
        for gift in list(gifts):
            self.receive_gift(gift)

    def receive_gift(self, gift):
        item = self._get_item_reader().get(gift.item)
        gift_name = u'подарок "' + str(gift.count)+' '+item.name + u"'"
        with_message = hasattr(gift, 'msg') and gift.msg != ''
        moved = hasattr(item, 'moved') and item.moved == True
        free = hasattr(gift, 'free') and gift.free
        if with_message:
            gift_name += u" с сообщением: '" + gift.msg + u"'"
        if moved:
            logger.info(u"П"+gift_name[1:]+ u"' нужно поместить")
        if free:
            gift_name = u'бесплатный ' + gift_name
        gift_name += u" от " + gift.user
        logger.info(u'Доступен ' + gift_name)
        if not moved:
            if not with_message or self._get_options()["with_messages"]:
                if free or self._get_options()["non_free"]:
					logger.info(u"Принимаю " + gift_name)
					apply_gift_event = GameApplyGiftEvent(GameGift(gift.id))
					self._get_events_sender().send_game_events([
														apply_gift_event])
                                               
#CR_01				Цемент
#CR_06				Металл
#CR_11				Доска
#CR_16				Шестерня
#CR_25				Стекло
#CR_44				Мир
#CR_70				Время

            if 0:
                if free and (gift.item<>'@CR_44'): # мир
                    self._get_events_sender().send_game_events([{"userId":[gift.user],"itemId":gift.item[1:],"type":"gifts","msg":None,"action":"sendFreeGifts"}])
                    logger.info(u"Подарок от %s отправлен обратно: %s"%(gift.user,gift_name))
        self.remove_gift_from_game_state(gift)

    def remove_gift_from_game_state(self, gift):
        for current_gift in list(self._get_game_state().get_state().gifts):
            if gift.id == current_gift.id:
                self._get_game_state().get_state().gifts.remove(current_gift)


class AddGiftEventHandler(object):
    def __init__(self, game_state):
        self.__game_state = game_state

    def handle(self, event):
        gift = event.gift
        self.append_gift_to_game_state(gift)

    def append_gift_to_game_state(self, gift):
        logger.info(u"Получен подарок.")
        self.__game_state.gifts.append(gift)


class CakesReceiverBot(BaseActor):
    def perform_action(self):
        # Пряники
        trees = self._get_game_location().\
                    get_all_objects_by_type('newYearTree')
        cakes_count = 0
        for tree in trees:
            for i in tree.users:
                cakes_count += 1
                apply_tree_event = {"type": "newYearTree",
                                    "action": "applyNewYearGift",
                                    "objId": tree.id,
                                    "index": 0}
                self._get_events_sender().send_game_events([apply_tree_event])
            tree.users = []
        if cakes_count > 0:
            logger.info(u"Собрали %d пряников" % cakes_count)