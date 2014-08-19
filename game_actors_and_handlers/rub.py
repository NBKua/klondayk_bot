# coding=utf-8
import logging
#import pdb
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)

class Rub(BaseActor):
    def get_object_type(self):
        return "chop"


    def perform_action(self):
        energy_count = self._get_game_state().get_state().energy
        action_chop=self._get_game_location().get_all_objects_by_type('chop')
        for resource in action_chop:
            if self._get_game_state().get_state().energy>= resource.chopCount: 
                for i in range(resource.chopCount):
                    rub_event = {"objId":resource.id,"type":"item","action":"chop"}
                    self._get_events_sender().send_game_events([rub_event])
                    self._get_game_state().get_state().energy-=1
                    logger.info(u'рубим'+str(resource.id))
                

                
