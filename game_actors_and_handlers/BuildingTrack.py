#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)

class BuildingTrack(BaseActor):

    def perform_action(self):
        location_id = "isle_wild"    # на каком острове
        free_x = 25             # Координаты пустого места
        free_y = 25
        min_money = 1500000 # оставляем денег
        num = 100              # партиями по ... шт.
        building_id = "D_TRACK_BAMBOO_1" # Настил

        if location_id == self._get_game_state().get_location_id():
            build_cost = self._get_item_reader().get(building_id).buyCoins            
            next_id = 0            
            for object in self._get_game_location().get_game_objects():
                if object.id > next_id: next_id = object.id
            next_id += 1
            buy_track = {"x":free_x,"action":"buy","y":free_y,"itemId":building_id,"type":"item","objId":next_id}
            sell_track = {"action":"sell","type":"item","objId":next_id}
            track_events = []
            for n in range(num):
                track_events.append(buy_track)
                track_events.append(sell_track)
            #print 'track_events ',track_events    
            expa = 0    
            #while (self._get_game_state().get_state().gameMoney > (1000000000+build_cost*num)):
            while self._get_game_state().get_state().gameMoney > min_money:
                expa += 1
                logger.info(u'Покупаем настилы' +str(num)+ u'штук '  +str(expa)+ u'раз(а)')
                self._get_events_sender().send_game_events(track_events)
                self._get_game_state().get_state().gameMoney -= (build_cost-50)*num
                logger.info(u"Обменяли" +str(num*expa)+ u'штук на'  +str(10*num*expa)+ u'опыта')