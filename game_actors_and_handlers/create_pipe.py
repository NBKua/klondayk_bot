# coding=utf-8
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class CreatePipe(BaseActor):
    
    def perform_action(self):
        object_id = self.get_building_id("@B_SKLEP")
        if object_id:
            print "CSKLEP"
            crafts = self._get_item_reader().get("B_SKLEP").crafts
            collections = self._get_game_state().get_state().collectionItems
            for craft in crafts:
                #craft_id = craft.id
                craft_id = 3
                while self.craft_is_possible(craft, collections):
                    self.make_craft(craft_id, object_id)
                    logger.info(u'Создаем %s' % (craft.name))
                    for material in craft.materials:
                       self.decrement_material(material, collections)
                       
    def decrement_material(self, material, collections):
        new_count = getattr(collections, self._get_item_reader().get(material.item).id, 0) - material.count
        setattr(collections, self._get_item_reader().get(material.item).id, new_count)
                    
    def get_building_id(self, building_type):
            for item in self._get_game_state().get_state().gameObjects:
                if item.item == building_type:
                    return item.id
                
    def craft_is_possible(self, craft, collections):
        first_coll = craft.materials[0].item
        first_coll_count = craft.materials[0].count
        second_coll = craft.materials[1].item
        second_coll_count = craft.materials[1].count
        storage_coll1 = getattr(collections, self._get_item_reader().get(first_coll).id, 0)
        storage_coll2 = getattr(collections, self._get_item_reader().get(second_coll).id, 0)
#        print storage_coll1
        return first_coll_count <= storage_coll1 and second_coll_count <= storage_coll2
                
    def make_craft(self, craft_id, object_id):
                event = {"itemId":craft_id,"objId":object_id,"type":"item","action":"craft"}
                self._get_events_sender().send_game_events([event])
