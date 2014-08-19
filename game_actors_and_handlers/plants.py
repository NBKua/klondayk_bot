# coding=utf-8
import logging
from game_state.game_types import GamePlant, GameFruitTree, GameSlag,\
    GameDigItem, GamePickItem, GameBuyItem, GameSellItem, GameUseStorageItem, GameFertilizeTree
from game_state.item_reader import LogicalItemReader
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict
logger = logging.getLogger(__name__)

class FertilBot(BaseActor):
    
    def perform_action(self):
        fertil='@RED_TREE_FERTILIZER'
        fertil_count=self._get_game_state().count_in_storage(fertil)
        if (fertil_count==None) or(fertil_count==0):
            #logger.info(u'Нет удобрений')
            return
        fl_count=fertil_count
        logger.info(u'Имеются удобрения в количестве: %d' % (fertil_count))
        harvestItems = self._get_game_location().get_all_objects_by_type(GameFruitTree.type)
        fert_all = []
        for harvestItem in list(harvestItems):
            if not self._get_timer().has_elapsed(harvestItem.jobFinishTime):
                if not harvestItem.fertilized:
                    if harvestItem.type == GameFruitTree.type:
                        if fl_count>0:
                            fert_event = GameFertilizeTree(itemId = unicode(fertil[1:]), objId = harvestItem.id) 
                            harvestItem.jobFinishTime = self._get_timer()._get_current_client_time()
                            harvestItem.fertilized = True
                            fert_all += [fert_event]
                            fl_count -= 1
        if len(fert_all)>0:
            self._get_events_sender().send_game_events(fert_all)
            logger.info(u'Удобрено %d деревьев' % (fertil_count-fl_count))
            self._get_game_state().remove_from_storage(fertil,fertil_count-fl_count)

class UseEggItemBot(BaseActor):

    def perform_action(self):
        '''use_items ={
		#'EGG_01':10, 					#Бэйби-сюрприз
		#'EGG_02':10, 					#Простое
		#'EGG_03':10, 					#Непростое
		#'EGG_04':10, 					#Русское
		#'EGG_05':10, 					#Пингвин-яйцо
		#'EGG_07':10, 					#Ромашковое
		#'EGG_08':10, 					#Сердешное
		#'EGG_09':10, 					#Глазное
		#'EGG_10':10, 					#Медовое
		#'EGG_11':10, 					#Цитрусовое
		#'EGG_12':10, 					#Цветное
		#'EGG_13':10, 					#Детское
		#'EGG_15':10, 					#Звёздное
		#'EGG_16':10, 					#Расписное
		#'EGG_17':10, 					#Васильковое
		#'EGG_18':10, 					#Строгое
		#'EGG_19':10,					#Ананасное
		#'EGG_20':10, 					#Клубничное
		#'EGG_21':10, 					#Арбузное
		#'EGG_22':10, 					#Вейдер-сюрприз   
		#'EGG_33':10, 					#Полосатое   #Добавил я Cheat Cheater
		#'EGG_34':10, 					#Сюрприз повара   #Добавил я Cheat Cheater
		#'EGG_31':10, 					#Рогатое   #Добавил я Cheat Cheater
		#'EGG_10':10, 					#Медовое   #Добавил я Cheat Cheater
		#'EGG_24':10, 					#Картман-сюрприз   #Добавил я Cheat Cheater
		#'EGG_06':10,					#'EGG_06' Зомби сюрприз  #Добавил я Cheat Cheater
		#'EGG_27':10, 					#Губка-сюрприз   #Добавил я Cheat Cheater
		#'EGG_25':10, 					#Дизайнерское   #Добавил я Cheat Cheater
		#'EGG_26':10, 					#Термо яйцо     #Добавил я Cheat Cheater
		#'EGG_23':10, 					#Бендер сюрприз  #Добавил я Cheat Cheater
		#'WEALTH_BOTTLE':10, 			        #Бутылка #Добавил я Cheat Cheater
		#'WEALTH_ROLL':10,   			        #Свиток  #Добавил я Cheat Cheater
		#'WEALTH_VASE':10,   			        #Ваза    #Добавил я Cheat Cheater
		#'WEALTH_BOWL':10,   			        #Чаша    #Добавил я Cheat Cheater
		#'WEALTH_SEQ':10,  			        #Связка бррёвен секвойи   #Добавил я Cheat Cheater
		#'WEALTH_CASKET':10, 			        #Шкатулка   #Добавил я Cheat Cheater
		#'WEALTH_WOODPALM':10, 		                #Связка брёвен пальмы   #Добавил я Cheat Cheater
		#'WEALTH_WHITEM':10, 			        #Груда белого мрамора  #Добавил я Cheat Cheater
		#'WEALTH_BLACKM':10, 			        #Груда черного мрамора   #Добавил я Cheat Cheater
		#'WEALTH_MARBLE':10, 			        #Груда зеленого мрамора  #Добавил я Cheat Cheater
		#'WEALTH_SKULL':10,  			        #Череп  #Добавил я Cheat Cheater
		#'SOCK_NY_BIG':10, 			#Носок Изобилия   #Добавил я Cheat Cheater
                #'SOCK_NY_MIDDLE':10, 			#Полярный носок  #Добавил я Cheat Cheater
		#'TURKEY_BOX':10,     			#Пернатый подарок  #Добавил я Cheat Cheater
		#'MONSTER_BOX_0':10, 			#Сундук чудовища
		#'MONSTER_BOX_1':10, 			#Сундук чудовища
		#'MONSTER_BOX_2':10, 			#Сундук чудовища
		#'MONSTER_BOX_3':10, 			#Сундук чудовища
		#'MONSTER_BOX_4':10, 			#Сундук чудовища
		#'WEALTH_CONE':10,   			#шишка
		#'FREE_NY_BOX':10, 			#сюрприз
		#'WEALTH_MITTENS':10, 			#варежки
		#'WEALTH_PITCHER':10, 			#кувшин
		#'WEALTH_LARGEBARREL':10, 		#большая бочка
		}'''
        use_items = {"WEALTH_SWORD",'CAT_BOX','WEALTH_POISON','CANDY_BOX3','BOUQUET_TULIPS','BOUQUET_MIMOSA','CANDY_BOX1','WEALTH_LARGEBARREL','WEALTH_PITCHER','WEALTH_MITTENS','FREE_NY_BOX','WEALTH_CONE','TURKEY_BOX','WEALTH_SKULL','SOCK_NY_MIDDLE_BOX','SOCK_NY_BIG_BOX','EGG_33','EGG_34','EGG_23','WEALTH_MARBLE','WEALTH_BLACKM','WEALTH_WHITEM','WEALTH_WOODPALM','WEALTH_CASKET','WEALTH_SEQ','WEALTH_BOWL','WEALTH_VASE','WEALTH_ROLL','WEALTH_BOTTLE','EGG_01','EGG_02','EGG_03','EGG_04','EGG_05','EGG_07','EGG_08','EGG_09','EGG_10','EGG_11','EGG_12','EGG_13','EGG_15','EGG_16','EGG_17','EGG_18','EGG_19','EGG_20','EGG_21','EGG_22','EGG_25','EGG_26','MONSTER_BOX_0','MONSTER_BOX_1','MONSTER_BOX_2','MONSTER_BOX_3','MONSTER_BOX_4'}
        for use_item in use_items:
            got_items=self._get_game_state().count_in_storage('@'+use_item)
            if got_items>0:
                logger.info(u'Бьем "%s" в количестве = %d' % (self._get_item_reader().get(use_item).name, got_items))
                col=got_items/10
                for i in range(col):
                    for j in range(10):
                        #sell_event = {"x":10,"action":"useStorageItem","y":10,"itemId":use_item,"type":"item"}
                        sell_event = GameUseStorageItem(itemId=unicode(use_item), y=long(10), x=long(10))
                        self._get_events_sender().send_game_events([sell_event])
                        self._get_game_state().remove_from_storage('@'+use_item,1)
                if (got_items-(col*10))>0:
                    events=[]
                    for j in range(got_items-(col*10)):
                        sell_event = GameUseStorageItem(itemId=unicode(use_item), y=long(10), x=long(10))
                        self._get_events_sender().send_game_events([sell_event])
                        self._get_game_state().remove_from_storage('@'+use_item,1)
                logger.info(u'Разбито %d "%s"' % (got_items, self._get_item_reader().get(use_item).name))

class HarvesterBot(BaseActor):

    def perform_action(self):
        # Растения
        plants = self._get_game_location().get_all_objects_by_type(
            GamePlant.type)
        # Деревья
        trees = self._get_game_location().get_all_objects_by_type(
            GameFruitTree.type)
            
        harvestItems = plants + trees
        pick_name={}
        pick_events = []

        for harvestItem in list(harvestItems):
            pick_event = self._pick_harvest(harvestItem,pick_name)
            if pick_event:
                pick_events.append(pick_event)
        if len(pick_name.keys())>0:
            for i in pick_name.keys():
                logger.info(u"Собрали %d '%s'"%(pick_name[i],i))
            self._get_events_sender().send_game_events(pick_events)

        slags = self._get_game_location().get_all_objects_by_type(
            GameSlag.type)
        dig_events = []
        dig_name={}
        for slag in list(slags):
            item = self._get_item_reader().get(slag.item)
            if item.name in dig_name.keys(): dig_name[item.name]+=1
            else: dig_name[item.name]=1
            dig_event = GameDigItem(slag.id)
            dig_events.append(dig_event)
            # convert slag to ground
            slag.type = 'base'
            slag.item = '@GROUND'
        if len(dig_name.keys())<>0:
            self._get_events_sender().send_game_events(dig_events)
            for i in dig_name.keys():
                logger.info(u"Вскопали %d '%s'"%(dig_name[i],i))

    def _pick_harvest(self, harvestItem,pick_name):
        if self._get_timer().has_elapsed(harvestItem.jobFinishTime):
            item = self._get_item_reader().get(harvestItem.item)
            
            if item.name in pick_name.keys(): pick_name[item.name]+=1
            else: pick_name[item.name]=1
            pick_event = GamePickItem(objId=harvestItem.id)

            # Добавляем в game_state информацию о собранном предмете
            item_count=0
            if harvestItem.type == GameFruitTree.type:
                item_id=self._get_item_reader().get(harvestItem.item).storageItem
                
            else: item_id=harvestItem.item
            #item_id = '@S'+item_id[2:]
            #item_id= self._get_game_state().seed2storage_plant(item_id)
            
            #print item_id
            self._get_game_state().add_from_storage(item_id,1)
            
            # Если собрали золиан - удалить обьект т.к. грядки больше нет
            if harvestItem.item in u'@P_43':
                self._get_game_location().remove_object_by_id(harvestItem.id)
                
            if harvestItem.type == GamePlant.type:
                # convert plant to slag
                harvestItem.type = GameSlag.type
                harvestItem.item = GameSlag(0L, 0L, 0L).item
            elif harvestItem.type == GameFruitTree.type:
                harvestItem.fruitingCount -= 1
                #self._get_timer().has_elapsed(harvestItem.jobFinishTime)
                
                if harvestItem.fruitingCount == 0:
                    
                    # remove fruit tree
                    self._get_game_location().remove_object_by_id(
                                                                harvestItem.id)
                    pickup_box = dict2obj({'item': '@FT_PICKUP_BOX_' + harvestItem.item[4:],'type': "pickup",'id': harvestItem.id, u'y': harvestItem.y, u'x': harvestItem.x})  
                    self._get_game_location().append_object(pickup_box)
                    #print u'Сундук'  
                    # harvestItem.type = GamePickItem.type
                    # TODO convert to pickup box
                    # convert tree to pick item
            return pick_event


class SeederBot(BaseActor):

    def perform_action(self):

        seed_items = self._get_options()
        if (seed_items<>None) and (seed_items<>'None'):
            buy_events = []
            grounds = self._get_game_location().get_all_objects_by_type('ground')
            location = self._get_game_state().get_game_loc().get_location_id()
            if type(seed_items)==type(''): seed_item = self._get_item_reader().get(seed_items)
            elif type(seed_items)==type({}):
                if location in seed_items.keys(): seed_id = seed_items[location]
                else: seed_id = seed_items['other']
                if seed_id=='None': return
                seed_item = self._get_item_reader().get(seed_id)
            else: seed_item=seed_items

#            
#            if time_harvest<28421 :
#                logger.info(u'Осталось 5-мин урожая: %d' % (int(time_harvest)))
#                seed_item.id='P_39'
#                logger.info(u'Сеем: %s' % (seed_items.id))

            if not self._is_seed_available(seed_item):
                logger.info(u'Это растение здесь сажать запрещено')
                return
            all_event = []
            for ground in list(grounds):
                item = self._get_item_reader().get(ground.item)
                buy_event = GameBuyItem(unicode(seed_item.id),
                                        ground.id,
                                        ground.y, ground.x)
                all_event += [buy_event]
                buy_events.append(buy_event)
                ground.type = u'plant'
                ground.item = unicode(seed_item.id)

            if len(all_event)>0:
                self._get_events_sender().send_game_events(buy_events)
                logger.info(u'Посеяли %d "%s"'%(len(all_event),seed_item.name))

    def _is_seed_available(self, seed_item):
        seed_reader = GameSeedReader(self._get_item_reader())
        game_state = self._get_game_state()
        return seed_reader.is_item_available(seed_item, game_state)


class GameSeedReader(LogicalItemReader):

    def _get_item_type(self):
        return 'seed'

    def _get_all_item_ids(self):
        return self._item_reader.get('shop').seed


class PlantEventHandler(object):
    def __init__(self, game_location):
        self.__game_location = game_location

    def handle(self, event_to_handle):
        gameObject = self.__game_location.get_object_by_id(
            event_to_handle.objId
        )
        if gameObject is None:
            logger.critical("OMG! No such object")
            return
        else:
            gameObject.fertilized = True
            #logger.info(u'Растение посажено')
            gameObject.jobFinishTime = event_to_handle.jobFinishTime
            gameObject.jobStartTime = event_to_handle.jobStartTime
