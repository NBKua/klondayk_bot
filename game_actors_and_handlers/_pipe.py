# coding=utf-8
# Обмен роз и лилий в Бизнес-Центре на деньги
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class Pipe(BaseActor):

    def perform_action(self):
        if self._get_game_state().get_state().gameMoney < 100000000:
            current_loc = self._get_game_state().get_location_id()
            #location_id = "isle_02"
            #if current_loc == location_id:
            craft = "3"
            exchange = self._get_item_reader().get("B_BUSINESS").crafts
            for one_item in exchange:
                    if one_item.id == craft:
                        rose = one_item.materials[0].item
                        rose_count = one_item.materials[0].count
                        lily = one_item.materials[1].item
                        lily_count = one_item.materials[0].count
                        result = one_item.resultCount
                        print result
            storage = self._get_game_state().get_state().storageItems
            for item in storage:
                    if item.item == rose:
                        storage_rose = item.count
                    elif item.item == lily:
                        storage_lily = item.count
            for item in self._get_game_state().get_state().gameObjects:
                    if item.item == "@B_BUSINESS":
                        o_id = item.id
            for _ in range(5000):
                    if storage_rose > rose_count and storage_lily > lily_count:
                        event = {"itemId":craft,"objId":o_id,"action":"craft","type":"item"}
                        logger.info("Обмениваем партию Роз и Лилий")
                        print event
                        self._get_events_sender().send_game_events([event])
                        self._get_game_state().get_state().gameMoney += result
                        storage_rose -= rose_count
                        storage_lily -= lily_count