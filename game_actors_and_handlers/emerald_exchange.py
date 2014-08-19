# coding=utf-8
import logging
from math import ceil
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict


logger = logging.getLogger(__name__)

class Emeraldic(BaseActor):

    #функция создания чего-либо
    def create_items (self, _obj_id,_item_id):
        create_items_event = {"type": "item",
                               "action": "craft",
                               "objId": _obj_id,
                               "itemId":_item_id}
        self.events_append(create_items_event)
    
    def events_append(self, event):
        self._events.append(event)
        if len(self._events) > 499:
            self.events_free()

    def events_free(self):
        if self._events != []: self._get_events_sender().send_game_events(self._events)
        self._events = []

    def perform_action(self):
        min_coll = 500               # Оставляем ручных и обувных коллекций
        dread = 1                       # Страшная
        luksor = 1                      # Луксорская
        location_id = u'isle_ufo'   # на каком острове
        
        #-----------------------------------------------------------------------
        # обмен коллекций
        _loc = self._get_game_state().get_game_loc().get_location_id()
        if _loc != location_id: return 1

        self._events = []                                                   
        obj_id_iz_melnica = obj_id_iz_majak = ''
        #получаем id
        buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type) 
        for building in list(buildings): 
            if building.item == '@B_MILL_EMERALD2':
                obj_id_iz_melnica = building.id
            if building.item == '@B_LIGHT_EMERALD2':
                obj_id_iz_majak = building.id

        if obj_id_iz_melnica == '' and obj_id_iz_majak == '': return 1

        cl_items = obj2dict(self._get_game_state().get_state().collectionItems)
        #self._get_game_state().get_state().collectionItems
        hand_1 = hand_2 = hand_3 = hand_4 = hand_5 = 0
        shoe_1 = shoe_2 = shoe_3 = shoe_4 = shoe_5 = 0
        bike_1 = bike_2 = bike_3 = bike_4 = bike_5 = 0
        znak_1 = znak_2 = znak_3 = znak_4 = znak_5 = 0
        for _item in cl_items.keys():
            if _item == 'C_5_1':   hand_1 = cl_items[_item]   # Ручная
            if _item == 'C_5_2':   hand_2 = cl_items[_item]   # Ручная
            if _item == 'C_5_3':   hand_3 = cl_items[_item]   # Ручная
            if _item == 'C_5_4':   hand_4 = cl_items[_item]   # Ручная
            if _item == 'C_5_5':   hand_5 = cl_items[_item]   # Ручная
            
            if _item == 'C_6_1':   shoe_1 = cl_items[_item]   # Обувная
            if _item == 'C_6_2':   shoe_2 = cl_items[_item]   # Обувная
            if _item == 'C_6_3':   shoe_3 = cl_items[_item]   # Обувная
            if _item == 'C_6_4':   shoe_4 = cl_items[_item]   # Обувная
            if _item == 'C_6_5':   shoe_5 = cl_items[_item]   # Обувная

            if _item == 'C_3_1':   bike_1 = cl_items[_item]   # Байкерская
            if _item == 'C_3_2':   bike_2 = cl_items[_item]   # Байкерская
            if _item == 'C_3_3':   bike_3 = cl_items[_item]   # Байкерская
            if _item == 'C_3_4':   bike_4 = cl_items[_item]   # Байкерская
            if _item == 'C_3_5':   bike_5 = cl_items[_item]   # Байкерская
            
            if _item == 'C_4_1':   znak_1 = cl_items[_item]   # Знаков
            if _item == 'C_4_2':   znak_2 = cl_items[_item]   # Знаков
            if _item == 'C_4_3':   znak_3 = cl_items[_item]   # Знаков
            if _item == 'C_4_4':   znak_4 = cl_items[_item]   # Знаков
            if _item == 'C_4_5':   znak_5 = cl_items[_item]   # Знаков       

        # Страшная
        if(obj_id_iz_melnica != '') and dread:
            if (hand_1 > min_coll and shoe_1 > min_coll) or (hand_2 > min_coll and shoe_2 > min_coll) or (hand_3 > min_coll and shoe_3 > min_coll) or (hand_4 > min_coll and shoe_4 > min_coll):
                print
                print u'Ручная:    ', str(hand_1).rjust(6, ' ')+',', str(hand_2).rjust(6, ' ')+',', str(hand_3).rjust(6, ' ')+',', str(hand_4).rjust(6, ' ')+',', str(hand_5).rjust(6, ' ')
                print u'Обувная:   ', str(shoe_1).rjust(6, ' ')+',', str(shoe_2).rjust(6, ' ')+',', str(shoe_3).rjust(6, ' ')+',', str(shoe_4).rjust(6, ' ')+',', str(shoe_5).rjust(6, ' ') 
            if hand_1 > min_coll and shoe_1 > min_coll:
                if hand_1 > shoe_1:
                    count = shoe_1 - min_coll 
                else:
                    count = hand_1 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_melnica, "1")
                cl_items['C_5_1'] -= count
                cl_items['C_6_1'] -= count
                logger.info(u'Создали %d перчаток Фредди', i + 1)
                if 'C_7_1' in cl_items.keys():
                    cl_items['C_7_1'] += count
                else:cl_items['C_7_1'] = count
                
            if hand_2 > min_coll and shoe_2 > min_coll:
                if hand_2 > shoe_2:
                    count = shoe_2 - min_coll
                else:
                    count = hand_2 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_melnica, "2")
                cl_items['C_5_2'] -= count
                cl_items['C_6_2'] -= count
                logger.info(u'Создали %d шляп Фредди', i + 1)
                if 'C_7_2' in cl_items.keys():
                    cl_items['C_7_2'] += count
                else:cl_items['C_7_2'] = count
                
            if hand_3 > min_coll and shoe_3 > min_coll: 
                if hand_3 > shoe_3: 
                    count = shoe_3 - min_coll
                else:
                    count = hand_3 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_melnica, "3")
                cl_items['C_5_3'] -= count
                cl_items['C_6_3'] -= count
                logger.info(u'Создали %d кофт Фредди', i + 1)
                if 'C_7_3' in cl_items.keys():
                    cl_items['C_7_3'] += count
                else:cl_items['C_7_3'] = count
                
            if hand_4 > min_coll and shoe_4 > min_coll: 
                if hand_4 > shoe_4:
                    count = shoe_4 - min_coll
                else:
                    count = hand_4 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_melnica, "4")
                cl_items['C_5_4'] -= count
                cl_items['C_6_4'] -= count
                logger.info(u'Создали %d зажигалок Фредди', i + 1)
                if 'C_7_4' in cl_items.keys():
                    cl_items['C_7_4'] += count
                else:cl_items['C_7_4'] = count
                
            if hand_5 > min_coll and shoe_5 > min_coll:
                if hand_5 > shoe_5: 
                    count = shoe_5 - min_coll 
                else:
                    count = hand_5 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_melnica, "5")
                cl_items['C_5_5'] -= count
                cl_items['C_6_5'] -= count
                logger.info(u'Создали %d будильников Фредди', i + 1)
                if 'C_7_5' in cl_items.keys():
                    cl_items['C_7_5'] += count
                else:cl_items['C_7_5'] = count
            
        #Луксорская
        if(obj_id_iz_majak != '') and luksor:
            if (bike_1 > min_coll and znak_1 > min_coll) or (bike_2 > min_coll and znak_2 > min_coll) or (bike_3 > min_coll and znak_3 > min_coll) or (bike_4 > min_coll and znak_4 > min_coll):
                print
                print u'Байкерская:', str(bike_1).rjust(6, ' ')+',', str(bike_2).rjust(6, ' ')+',', str(bike_3).rjust(6, ' ')+',', str(bike_4).rjust(6, ' ')+',', str(bike_5).rjust(6, ' ')
                print u'Знаков:    ', str(znak_1).rjust(6, ' ')+',', str(znak_2).rjust(6, ' ')+',', str(znak_3).rjust(6, ' ')+',', str(znak_4).rjust(6, ' ')+',', str(znak_5).rjust(6, ' ')
            if bike_1 > min_coll and znak_1 > min_coll:
                if bike_1 > znak_1:
                    count = znak_1 - min_coll 
                else:
                    count = bike_1 - min_coll 
                for i in range(count):
                    self.create_items(obj_id_iz_majak, "1") 
                cl_items['C_3_1'] -= count
                cl_items['C_4_1'] -= count
                logger.info(u'Создали %d "Бинты мумии"', i + 1)
                if 'C_2_1' in cl_items.keys():
                    cl_items['C_2_1'] += count
                else:cl_items['C_2_1'] = count
                
            if bike_2 > min_coll and znak_2 > min_coll: 
                if bike_2 > znak_2:
                    count = znak_2 - min_coll
                else:
                    count = bike_2 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_majak, "2")
                cl_items['C_3_2'] -= count
                cl_items['C_4_2'] -= count
                logger.info(u'Создали %d "Гребешок"', i + 1)
                if 'C_2_2' in cl_items.keys():
                    cl_items['C_2_2'] += count
                else:cl_items['C_2_2'] = count
                
            if bike_3 > min_coll and znak_3 > min_coll:
                if bike_3 > znak_3:
                    count = znak_3 - min_coll
                else:
                    count = bike_3 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_majak, "3")
                cl_items['C_3_3'] -= count
                cl_items['C_4_3'] -= count
                logger.info(u'Создали %d "Кошечка"', i + 1)
                if 'C_2_3' in cl_items.keys():
                    cl_items['C_2_3'] += count
                else:cl_items['C_2_3'] = count
                 
            if bike_4 > min_coll and znak_4 > min_coll:
                if bike_4 > znak_4:
                    count = znak_4 - min_coll
                else:
                    count = bike_4 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_majak, "4")
                cl_items['C_3_4'] -= count
                cl_items['C_4_4'] -= count
                logger.info(u'Создали %d "Скарабей"', i + 1)
                if 'C_2_4' in cl_items.keys():
                    cl_items['C_2_4'] += count
                else:cl_items['C_2_4'] = count
                  
            if bike_5 > min_coll and znak_5 > min_coll:
                if bike_5 > znak_5:
                    count = znak_5 - min_coll
                else:
                    count = bike_5 - min_coll
                for i in range(count):
                    self.create_items(obj_id_iz_majak, "5")
                cl_items['C_3_5'] -= count
                cl_items['C_4_5'] -= count
                logger.info(u'Создали %d "Фараон"', i + 1)
                if 'C_2_5' in cl_items.keys():
                    cl_items['C_2_5'] += count
                else:cl_items['C_2_5'] = count

        print
        self.events_free()
        self._get_game_state().get_state().collectionItems=dict2obj(cl_items)
