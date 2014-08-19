# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup
from game_state.game_event import dict2obj
from game_actors_and_handlers.workers import TargetSelecter
from game_actors_and_handlers.workers import ResourcePicker

logger = logging.getLogger(__name__)


class WoodTargetSelecter(TargetSelecter):

    def get_worker_types(self):
        return [GameWoodGrave.type, GameWoodGraveDouble.type]

    def get_object_type(self):
        return GameWoodTree.type

    def get_sent_job(self):
        return "Рубим дерево"


class WoodPicker(ResourcePicker):

    def get_worker_types(self):
        return [GameWoodGrave.type, GameWoodGraveDouble.type]



        #Забираем продукцию с Лесопилки
        wood_graves = self._get_game_location().get_all_objects_by_types('woodGainBuilding')
        for wood in wood_graves:
            if wood.materials!=[]:
                for material_id in list(wood.materials):
                    material = self._get_item_reader().get(material_id.item[1:])
                    name = material.name
                    logger.info(u'Забираем ' + name.upper())
                    event_pick={"type":"item","count":1,"objId":wood.id,"action":"pick","itemId":material_id.item[1:]}
                    self._get_events_sender().send_game_events([event_pick])
                    self._get_game_state().add_from_storage(material_id.item,1)
                    wood.materials.remove(material_id) 
