# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor
logger = logging.getLogger(__name__)


class BowReceiverBot(BaseActor):
    def perform_action(self):
        # бантики
        bows = self._get_game_location().\
                    get_all_objects_by_type('halloweenTower')
                    
        if not hasattr(self._get_game_state(), 'circus_user'):
            try:
                with open('circus_user.txt', 'r') as f:
                    self._get_game_state().circus_user = eval(f.read())
            except:
                self._get_game_state().circus_user = []                    

        self._event = []
        self.bow_count = 0
        for bow in bows:
            if bow.item == '@B_TENT_CIRCUS':
                for i in bow.users:
                    self._get_game_state().circus_user.append(i.id)
                    self._event.append({"extraId":i.id,"itemId":i.itemId,"action":"trick","type":"item","objId":bow.id})
                    if i.itemId == u'BOW_PACK_DEFAULT':
                        count = 1
                    elif i.itemId == u'BOW_PACK_SMALL':
                        count = 3
                    elif i.itemId == u'BOW_PACK_MEDIUM':
                        count = 10
                    self.bow_count += count
                    if len(self._event) > 499:
                        self.events_send()
                bow.users = []
                self.events_send()
                
    def events_send(self):
        if self._event != []:
            self._get_events_sender().send_game_events(self._event)
            # добавляем на склад
            self._get_game_state().add_from_storage("@CR_153",self.bow_count)
            with open('circus_user.txt', 'w') as f:
                f.write(str(self._get_game_state().circus_user))
            print
            if str(len(self._event))[-1:] == '1' and len(self._event) !=11:
                if str(self.bow_count)[-1:] == '1' and self.bow_count !=11:
                    logger.info(u'Собрали %d бантик   от %d друга' % (self.bow_count, len(self._event)))
                elif 1 < int(str(self.bow_count)[-1:]) < 5 and self.bow_count < 5 and self.bow_count > 20:
                    logger.info(u'Собрали %d бантика  от %d друга' % (self.bow_count, len(self._event)))
                else:
                    logger.info(u'Собрали %d бантиков от %d друга' % (self.bow_count, len(self._event)))
            else:
                if str(self.bow_count)[-1:] == '1' and self.bow_count !=11:
                    logger.info(u'Собрали %d бантик   от %d друзей' % (self.bow_count, len(self._event)))
                elif 1 < int(str(self.bow_count)[-1:]) < 5 and self.bow_count < 5 and self.bow_count > 20:
                    logger.info(u'Собрали %d бантика  от %d друзей' % (self.bow_count, len(self._event)))
                else:
                    logger.info(u'Собрали %d бантиков от %d друзей' % (self.bow_count, len(self._event)))
            self._event = []
            self.bow_count = 0