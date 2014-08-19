# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)

class VisitingUsers(BaseActor):
    
    def perform_action(self):
        frends_ids = self._get_options()
        print frends_ids[0]
        
        user_id = str(frends_ids[0])
        
        self._get_events_sender().send_game_events([{"type":"gameState","user":user_id,"locationId":"main","id":46667,"objId":None,"action":"gameState"}])
        logger.info(u'Посетил %s' % (user_id))
        # и домой
        self._get_events_sender().send_game_events([{"type":"gameState","user":None,"locationId":"main","id":46667,"objId":None,"action":"gameState"}])
        logger.info(u'Вернулся от %s' % (user_id))