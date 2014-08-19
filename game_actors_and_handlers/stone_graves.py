# coding=utf-8
import logging
from game_state.game_types import GameStoneGrave, GameStoneGraveDouble,\
    GamePickItem, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.workers import TargetSelecter
from game_actors_and_handlers.workers import ResourcePicker

logger = logging.getLogger(__name__)


class StoneTargetSelecter(TargetSelecter):

    def get_worker_types(self):
        return [GameStoneGrave.type, GameStoneGraveDouble.type]

    def get_object_type(self):
        return GameStone.type

    def get_sent_job(self):
        return "Добываем камень"


class StonePicker(ResourcePicker):

    def get_worker_types(self):
        return [GameStoneGrave.type, GameStoneGraveDouble.type]

