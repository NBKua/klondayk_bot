# coding=utf-8
import logging
from math import ceil
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict


logger = logging.getLogger(__name__)

class GameBrains(BaseActor):

  #функция создания чего-либо
  def create_items (self, _obj_id,_item_id):
    create_items_event = {"type": "item",
                           "action": "craft",
                           "objId": _obj_id,
                           "itemId":_item_id}        
    self._get_events_sender().send_game_events([create_items_event])    
         
    

  def perform_action(self):             
  
    brains_const = 19
 # Указываем нужное постоянное количество без имеющихся у игрока бесплатных  
     
    max_need_helly = max_need_garliclily = 2 * brains_const # Максимально необходимое кол-во хеллии и чесночных лилий
    max_need_love = 10 * brains_const # Максимально необходимое кол-во любви
    max_need_clevhell = 4 * max_need_garliclily # Максимально необходимое кол-во клеверхелла
    max_need_clever = ceil(max_need_clevhell/20)*20 # Максимально необходимое кол-во клевера 
    max_need_squashhell = ceil(max_need_clevhell/10)*10 # Максимально необходимое кол-во тыквахелла
    max_need_garlic = max_need_lily = ceil(max_need_garliclily/40)*40 # Максимально необходимое кол-во лилий и чеснока       
    
    obj_id_1 = obj_id_2 = '' # Переменные для ID останкино и корабля
         
    helly = love = clevhell = garliclily = clever = squashhell = garlic = lily = 0
                                                                   
    _loc = self._get_game_state().get_game_loc().get_location_id()                                                      
    
    
    if _loc == u'main':         

      #получаем id останкино и летучего корабля
      buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type)
      
      for building in list(buildings):
        building_item = self._get_item_reader().get(building.item)
        if building_item.name == u'Останкино за монеты': # или if building_item.id == 'B_OSTANKINO'
          obj_id_1 = building.id
        if building_item.name == u'Летучий корабль': # или if building_item.id == 'D_SHIP'
          obj_id_2 = building.id
          
      st_items = self._get_game_state().get_state().storageItems
                
      for _item in list(st_items):
        if hasattr(_item, 'item'):                             
            #it_name = self._get_item_reader().get(_item.item)
            #print 'it ', _item.item, ' name  ', it_name.name
            # Определяем на складе количество:
            if _item.item == ('@R_12'):   helly = _item.count       # Хеллия               
            if _item.item == ('@CR_31'):  love = _item.count        # Любовь 
            
            if _item.item == ('@R_02'):   clevhell = _item.count    # Клеверхелл 
            if _item.item == ('@R_09'):   garliclily = _item.count  # Чесночная лилия 
            
            if _item.item == ('@S_14'):   squashhell = _item.count  # Тыквахелл
            if _item.item == ('@S_03'):   clever = _item.count      # Клевер
            if _item.item == ('@S_15'):   lily = _item.count        # Лилия
            if _item.item == ('@S_08'):   garlic = _item.count      # Чеснок
            
      if love < max_need_love : 
        logger.info(u'Не хватает любви для создания мозгов, накопайте еще %d шт.',max_need_love-love)      
        if helly < max_need_helly and obj_id_2 == '':                                           
          logger.info(u'Не хватает хеллии для создания мозгов, сварите еще %d шт.',max_need_helly-helly)
        return
      
      elif helly < max_need_helly and obj_id_2 == '':                                           
        logger.info(u'Не хватает хеллии для создания мозгов, сварите еще %d шт.',max_need_helly-helly)
        return  
          
      elif helly < max_need_helly and obj_id_2 != '': 
        print u'QQQ'
        
        if clevhell < max_need_clevhell:
          if (clever < max_need_clever) and (squashhell < max_need_squashhell):
            logger.info(u'Не хватает клевера, посадите еще %d шт.',max_need_clever-clever)
            logger.info(u'Не хватает тыквахелла, посадите еще %d шт.',max_need_squashhell-squashhell)
            return
          elif clever < max_need_clever:
            logger.info(u'Не хватает клевера, посадите еще %d шт.',max_need_clever-clever)
            return
          elif squashhell < max_need_squashhell:
            logger.info(u'Не хватает тыквахелла, посадите еще %d шт.',max_need_squashhell-squashhell)
            return
          else:
            _i=0
            for _i in range(ceil((max_need_clevhell-clevhell)/10)):
              self.create_items(obj_id_2, "1")      
              
        if garliclily < max_need_garliclily:
          if (garlic < max_need_garlic) and (lily < max_need_lily):
            logger.info(u'Не хватает чеснока, посадите еще %d шт.',max_need_garlic-garlic)
            logger.info(u'Не хватает лилий, посадите еще %d шт.',max_need_lily-lily)    
            return
          elif garlic < max_need_garlic:
            logger.info(u'Не хватает чеснока, посадите еще %d шт.',max_need_garlic-garlic)
            return
          elif lily < max_need_lily:
            logger.info(u'Не хватает лилий, посадите еще %d шт.',max_need_lily-lily)
            return
          else:
            _i=0
            for _i in range(ceil((max_need_garliclily-garliclily)/10)):
              self.create_items(obj_id_2, "2")                     
                  
        _i=0
        for _i in range(max_need_clevhell-clevhell):
            self.create_items(obj_id_2, "3")
        
        
      
      brains_buy = self._get_game_state().get_state().buyedBrains # Кол-во активаций мозгов (не самих мозгов)
      brains_curr = 0 # Счетчик кол-ва текущих мозгов      
      x=0 # Счетчик кол-ва мозгов с истечением времени < 5 мин.            

      if len(brains_buy)<>0:        
          for buyed_brain in brains_buy: 
              hf = buyed_brain.count
              brains_curr += hf 
              m = ((int(buyed_brain.endTime)/1000)/60)-((((int(buyed_brain.endTime)/1000)/60)/60)*60)
              h = ((int(buyed_brain.endTime)/1000)/60)/60                                            
              if h==0 and m<=5:
                x+=hf
                        
      # Разница между необходимыми и текущими мозгами. 
      brains_lacks = 0                                       
      if brains_curr < brains_const:            
        brains_lacks = brains_const - brains_curr  
                                                       
      brains_lx = x + brains_lacks 
           
      # Определяем предположительное необходимое ко-во мозгов.           
      brains_need = brains_curr - brains_lx   

      # Если меньше нужного постоянного, то создаем недостающие.
      if brains_need < brains_const:
          _i=0
          for _i in range(brains_lx):          
            self.create_items(obj_id_1, "1")                                       
            brains_buy.append(dict2obj({u'count': 1L, u'endTime': u'86400000'})) #Добавляем фейк в список купленных мозгов для увеличения счетчика
          logger.info (u'Создано мозгов - %d шт.', brains_lx)     