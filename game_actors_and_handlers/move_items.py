# coding=utf-8
import logging
from game_state.game_types import GameBuilding, GamePlayGame, DailyBonus
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import obj2dict, dict2obj

logger = logging.getLogger(__name__)


class MoveItem(BaseActor):
	def perform_action(self):
		#что-то в склад
		for object in self._get_game_location().get_game_objects():
			print 'object.item ', object.item
			print 'object.id ', object.id
		for object in self._get_game_location().get_game_objects():
			if hasattr(object, 'type'):
				if object.item == '@CH_BAMBOO_ONE' or object.item == '@CH_BAMBOO_ONE':
					print u'спиздели все на х..й!', object.item, ', id = ', object.id        
					self._get_events_sender().send_game_events([{"type":"item","action":"moveToStorage","objId":object.id}])
		raw_input('-------------   END   ---------------')