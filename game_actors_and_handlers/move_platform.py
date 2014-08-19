# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)

class Platform(BaseActor):

    def perform_action(self):
        object_id = self.get_decoration_id("@B_SPHINCS")
        if object_id:
            event = {"objId":object_id,"type":"item","action":"moveToStorage"}
            self._get_events_sender().send_game_events([event])
            logger.info(u"Спиздили перрон")

    def get_decoration_id(self, decoration_type):
            for item in self._get_game_state().get_state().gameObjects:
                if item.item == decoration_type:
                    return item.id
