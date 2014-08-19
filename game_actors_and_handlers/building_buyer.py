# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor
from game_state.brains import PlayerBrains

logger = logging.getLogger(__name__)

class BuildingBuyer(BaseActor):

    def perform_action(self):
        current_loc = self._get_game_state().get_location_id()
        location_id = "isle_omega"
        if current_loc == location_id:
            building_id = "B_ROCKET"
            money = self._get_game_state().get_state().gameMoney
            build_cost = self._get_item_reader().get(building_id).buyCoins
            next_id = self._get_game_state().get_state().gameObjects[-1].id + 1
            buy_rocket = {"x":21,"action":"buy","y":17,"itemId":building_id,"type":"item","objId":next_id}
            sell_rocket = {"action":"sell","type":"item","objId":next_id}
            for _ in range(90):
                if money > 10000000:
                #if money > build_cost or money > 1000000000 and occupied_brain_count < 9
                    logger.info(u"Покупаем ракету")
                    self._get_events_sender().send_game_events([buy_rocket])
                    logger.info(u"Продаём ракету")
                    self._get_events_sender().send_game_events([sell_rocket])
                    self._get_game_state().get_state().gameMoney -= build_cost