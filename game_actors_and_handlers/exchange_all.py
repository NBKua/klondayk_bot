# coding=utf-8
import logging
from math import ceil
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict


logger = logging.getLogger(__name__)

class GameBrains1(BaseActor):

  #функция создания чего-либо
  def create_items (self, _obj_id,_item_id):
    create_items_event = {"type": "item",
                           "action": "craft",
                           "objId": _obj_id,
                           "itemId":_item_id}        
    self.events_append(create_items_event)    
         
  def events_append(self, event):
    self._events.append(event)
    if len(self._events) > 9:
        self.events_free()

  def events_free(self):
    if self._events != []: self._get_events_sender().send_game_events(self._events)
    self._events = []

  def perform_action(self):

    min_coll = 1   # Оставляем ручных и обувных коллекций 

    _loc = self._get_game_state().get_game_loc().get_location_id()                                                      
    if not (_loc == u'main' or _loc == u'isle_ufo'):# выключать просто - изменяем ид острова на несуществующий и всё (isle_9elephant)
        return 1

    self._events = []
    # обмен коллекций                                                    
    if _loc == u'isle_ufo':
        obj_id_iz_melnica = obj_id_iz_majak = ''
        #получаем id
        buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type) 
        for building in list(buildings): 
            if building.item == '@B_MILL_EMERALD':# выключать просто - изменяем ид объекта на несуществующий и всё (B_MILL_9EMERALD2)
                obj_id_iz_melnica = building.id
            if building.item == '@B_LIGHT_EMERALD': 
                obj_id_iz_majak = building.id

        if(obj_id_iz_melnica != '' or obj_id_iz_majak != ''):

            cl_items = obj2dict(self._get_game_state().get_state().collectionItems)#self._get_game_state().get_state().collectionItems         
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

            #print 'Ручная:', hand_1, ',', hand_2, ',', hand_3, ',', hand_4, ',', hand_5, '; Обувная:', shoe_1, ',', shoe_2, ',', shoe_3, ',', shoe_4, ',', shoe_5
            #print 'Байкерская:', bike_1, ',', bike_2, ',', bike_3, ',', bike_4, ',', bike_5, '; Знаков:', znak_1, ',', znak_2, ',', znak_3, ',', znak_4, ',', znak_5
            #Стрёмная, очень...
            if(obj_id_iz_melnica != ''):
                if hand_1 > min_coll and shoe_1 > min_coll:
                    if hand_1 > shoe_1: 
                        count = shoe_1 - min_coll 
                    else: 
                        count = hand_1 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_melnica, "1") 
                        #logger.info(u'Создаём перчатку фреди %d', i + 1)    
                    logger.info(u'Создали %d перчаток Фредди', i + 1) 
                    
                if hand_2 > min_coll and shoe_2 > min_coll: 
                    if hand_2 > shoe_2: 
                        count = shoe_2 - min_coll 
                    else: 
                        count = hand_2 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_melnica, "2") 
                        #logger.info(u'Создаём шляпу фреди %d', i + 1) 
                    logger.info(u'Создали %d шляп Фредди', i + 1)                     
                    
                if hand_3 > min_coll and shoe_3 > min_coll: 
                    if hand_3 > shoe_3: 
                        count = shoe_3 - min_coll 
                    else: 
                        count = hand_3 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_melnica, "3") 
                        #logger.info(u'Создаём кофту фреди %d', i + 1)  
                    logger.info(u'Создали %d кофт Фредди', i + 1)                     
                     
                if hand_4 > min_coll and shoe_4 > min_coll: 
                    if hand_4 > shoe_4: 
                        count = shoe_4 - min_coll 
                    else: 
                        count = hand_4 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_melnica, "4")  
                        #logger.info(u'Создаём зажигалку фреди %d', i + 1)   
                    logger.info(u'Создали %d зажигалок Фредди', i + 1) 
                      
                if hand_5 > min_coll and shoe_5 > min_coll: 
                    if hand_5 > shoe_5: 
                        count = shoe_5 - min_coll 
                    else: 
                        count = hand_5 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_melnica, "5") 
                        #logger.info(u'Создаём будильник фреди %d', i + 1)  
                    logger.info(u'Создали %d будильников Фредди', i + 1)  
            #Луксорская
            if(obj_id_iz_majak != ''):
                if bike_1 > min_coll and znak_1 > min_coll:
                    if bike_1 > znak_1: 
                        count = znak_1 - min_coll 
                    else: 
                        count = bike_1 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_majak, "1") 
                        #logger.info(u'Создаём "Бинты мумии" %d', i + 1)    
                    logger.info(u'Создали %d "Бинты мумии"', i + 1) 
                    
                if bike_2 > min_coll and znak_2 > min_coll: 
                    if bike_2 > znak_2: 
                        count = znak_2 - min_coll 
                    else: 
                        count = bike_2 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_majak, "2") 
                        #logger.info(u'Создаём "Гребешок" %d', i + 1) 
                    logger.info(u'Создали %d "Гребешок"', i + 1)                     
                    
                if bike_3 > min_coll and znak_3 > min_coll: 
                    if bike_3 > znak_3: 
                        count = znak_3 - min_coll 
                    else: 
                        count = bike_3 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_majak, "3") 
                        #logger.info(u'Создаём "Кошечка" %d', i + 1)  
                    logger.info(u'Создали %d "Кошечка"', i + 1)                     
                     
                if bike_4 > min_coll and znak_4 > min_coll: 
                    if bike_4 > znak_4: 
                        count = znak_4 - min_coll 
                    else: 
                        count = bike_4 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_majak, "4")  
                        #logger.info(u'Создаём "Скарабей" %d', i + 1)   
                    logger.info(u'Создали %d "Скарабей"', i + 1) 
                      
                if bike_5 > min_coll and znak_5 > min_coll: 
                    if bike_5 > znak_5: 
                        count = znak_5 - min_coll 
                    else: 
                        count = bike_5 - min_coll      
                    for i in range(count): 
                        self.create_items(obj_id_iz_majak, "5") 
                        #logger.info(u'Создаём "Фараон" %d', i + 1)  
                    logger.info(u'Создали %d "Фараон"', i + 1)  
                    self.events_free()                    
                    return 1
    #обмен коллекций

    brains_const = 19 # Указываем нужное постоянное количество без имеющихся у игрока бесплатных  
    
    want_helly = 60  # Сколько хотим хеллий иметь
    want_kley  = 20  # Клея
    want_trans = 20  # Трансформаторов
    want_yekraska= 20# Краски жёлтой

    min_money = 1000000  # оставляем денег

    obj_id_ostankino = obj_id_korabl = obj_id_elka = obj_id_pirmida = obj_id_bashnya = obj_id_furgon = '' # Переменные для ID останкино и корабля
         
    helly = love = clevhell = garliclily = clever = squashhell = garlic = lily = kley = trans = yekraska = steklo = 0
                                                                   

    #получаем id останкино и летучего корабля
    buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type)
    
    for building in list(buildings):
        building_item = self._get_item_reader().get(building.item)
        if building_item.id == 'B_OSTANKINO': # или if building_item.id == 'B_OSTANKINO'
            obj_id_ostankino = building.id
        if building_item.name == u'Летучий корабль': # или if building_item.id == 'D_SHIP'
            obj_id_korabl = building.id
        if building_item.id == 'B_NYTREE':
            obj_id_elka = building.id
        if building_item.id == 'B_PYRAMID':
            obj_id_pirmida = building.id
        if building_item.id == 'B_PISA':
            obj_id_bashnya = building.id
        if building_item.id == 'B_VAN_ICE_CREAM':
            obj_id_furgon = building.id

    travel_time = -1
    for l in self._get_game_state().get_state().buffs.list:
        if 'BUFF_TRAVEL_TICKET_TIME' in l.item:
            exp_time = float(l.expire.endDate) # l.expire.type  (= time)
            if travel_time < exp_time :
                travel_time = exp_time
    if travel_time < 0 and obj_id_furgon != '':
        logger.info(u'Создаём баф путешествий') 
        self.create_items(obj_id_furgon, "1") 

    st_items = self._get_game_state().get_state().storageItems
    #with open('storage2.txt', 'w') as f:
    #    f.write(str(obj2dict(st_items)).encode('utf-8'))
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
            
            if _item.item == ('@CR_25'):   steklo = _item.count     # Стекло
            if _item.item == ('@CR_17'):   kley = _item.count       # Супер-клей
            if _item.item == ('@CR_23'):   trans = _item.count      # Трансформатор
            if _item.item == ('@CR_10'):   yekraska = _item.count   # Жёлтая краска


    need_kley = (want_kley) - kley
    if need_kley < 0: need_kley = 0
    need_trans = (need_kley + want_trans) - kley
    if need_trans < 0: need_trans = 0
    need_yekraska = (need_kley + want_yekraska) - yekraska
    if need_yekraska < 0: need_yekraska = 0

    need_helly = (2 * brains_const + want_helly + (need_kley*2) + (need_trans) + (need_yekraska)) - helly # Максимально необходимое кол-во хеллии
    if need_helly < 0: need_helly = 0
    need_garliclily = (need_helly) - garliclily # Максимально необходимое кол-во чесночных лилий
    if need_garliclily < 0: need_garliclily = 0

    need_love = (10 * brains_const)-love # Максимально необходимое кол-во любви
    need_clevhell = (4 * need_helly) - clevhell # Максимально необходимое кол-во клеверхелла
    if need_clevhell < 0: need_clevhell = 0
    need_clever = (int(ceil(need_clevhell/20)*20)) - clever # Максимально необходимое кол-во клевера
    need_squashhell = (int(ceil(need_clevhell/10)*10)) - squashhell # Максимально необходимое кол-во тыквахелла
    need_garlic = (int(ceil(need_garliclily/40)*40)) - garlic # Максимально необходимое кол-во чеснока
    need_lily = (int(ceil(need_garliclily/40)*40)) - lily # Максимально необходимое кол-во лилий
    i = 0
    if need_helly > 0:
        if(obj_id_korabl == ''):
            logger.info(u'Не хватает хеллий, сварите еще %d шт.',need_helly)
            return
        else:
            if need_clevhell > 0:
                if need_clever > 0:
                    logger.info(u'Не хватает клевера, посадите еще %d шт.',need_clever)
                    return
                elif need_squashhell > 0:
                    logger.info(u'Не хватает тыквахелла, посадите еще %d шт.',need_squashhell)
                    return
                for i in range(int(ceil((need_clevhell)/10))+1):
                    self.create_items(obj_id_korabl, "1") 
                if i > 0:
                        logger.info(u'Создали %d клеверхелла', i*10) 

            if need_garliclily > 0:
                if need_garlic > 0:
                    logger.info(u'Не хватает чеснока, посадите еще %d шт.',need_garlic)
                    return
                elif need_lily > 0:
                    logger.info(u'Не хватает лилий, посадите еще %d шт.',need_lily)
                    return
                else:
                    for i in range(int(ceil((need_garliclily)/10))+1):
                        self.create_items(obj_id_korabl, "2") 
                    if i > 0:
                        logger.info(u'Создали %d чесночных лилий', i*10) 

            for i in range(need_helly):
                self.create_items(obj_id_korabl, "3")   
            if i > 0:
                logger.info(u'Создали %d хеллий', i) 
        
    if need_yekraska > 0:
        if(obj_id_pirmida != ''):
            if (self._get_game_state().get_state().gameMoney - ((need_yekraska) * 1000)) < min_money:
                print u'Не хватает денег'
                return
            else:
                for i in range(need_yekraska):
                    self.create_items(obj_id_pirmida, "1")   
                if i > 0:
                    logger.info(u'Создали %d жёлтой краски', i)
                    
    if need_trans > 0:
        if(obj_id_bashnya != ''):
            if (need_trans) > steklo:
                print u'Не хватает стекла'
                return
            else:
                for i in range(need_trans):
                    self.create_items(obj_id_bashnya, "1")   
                if i > 0:
                    logger.info(u'Создали %d трансформаторов', i)
                    
    if need_kley > 0:
        if(obj_id_elka != ''):
            if 0:
                return
            else:
                for i in range(need_kley):
                    self.create_items(obj_id_elka, "1")   
                if i > 0:
                    logger.info(u'Создали %d клея', i)

    if need_love > 0: 
        logger.info(u'Не хватает любви для создания мозгов, накопайте еще %d шт.', need_love)      
        return
    
    brains_buy = self._get_game_state().get_state().buyedBrains # Кол-во активаций мозгов (не самих мозгов)
    brains_curr = 0 # Счетчик кол-ва текущих мозгов      
    x=0 # Счетчик кол-ва мозгов с истечением времени < 5 мин.            

    if len(brains_buy)<>0:        
        for buyed_brain in brains_buy: 
            hf = buyed_brain.count
            brains_curr += hf 
            m = ((int(buyed_brain.endTime)/1000)/60)-((((int(buyed_brain.endTime)/1000)/60)/60)*60)
            h = ((int(buyed_brain.endTime)/1000)/60)/60                                            
            if h==0 and m<=6:
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
            self.create_items(obj_id_ostankino, "1")                                       
            brains_buy.append(dict2obj({u'count': 1L, u'endTime': u'86400000'})) #Добавляем фейк в список купленных мозгов для увеличения счетчика
        logger.info (u'Создано мозгов - %d шт.', brains_lx)    
    self.events_free()