# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)


class ShovelsExchange(BaseActor):
	def perform_action(self):
		current_loc = self._get_game_state().get_location_id()
		location_id = "main"
		if current_loc == location_id:
			craft = '2'
			exchange = self._get_item_reader().get("B_EYE").crafts
            #for one_item in exchange:
			if one_item.id == craft:
					doska = one_item.materials[0].item
                    doska_count = one_item.materials[0].count
                    gvozdi = one_item.materials[1].item
                    gvozi_count = one_item.materials[1].count
                    result = one_item.resultCount
            storage = self._get_game_state().get_state().storageItems
            for item in storage:
				if hasattr(item, "item"):
                        if item.item == doska:
                            storage_doska = item.count
                        elif item.item == gvozdi:
                            storage_gvozdi = item.count   
            for item in self._get_game_state().get_state().gameObjects:  
				if item.item == "@B_EYE":
					o_id = item.id
			for _ in range(10000):
				if storage_gvozdi > gvozdi_count and storage_doski > doski_count:
					event = {"itemId":craft,"objId":o_id,"action":"craft","type":"item"}
					logger.info(u'Обмениваем партию Досок и Гвоздей на Лопаты.')	
					self._get_events_sender().send_game_events([event])
					self._get_game_state().remove_from_storage(doski, doski_count)
                    self._get_game_state().remove_from_storage(gvozdi, gvozdi_count)
                    storage_doski -= doski_count
                    storage_gvozdi -= gvozdi_count
                    logger.info(u"storage_doski ",+str(storage_doski))
                    logger.info(u"storage_gvozdi ",+str(storage_gvozdi))	
				
				
				
				
				
				               
