# coding=utf-8
import random
import ssl
import message_factory
from message_factory import Session
import vkontakte
from settings import Settings
import vkutils
import logging
import time
from game_state.item_reader import GameItemReader
from game_state.game_event import dict2obj, obj2dict
from game_state.game_types import GameEVT, GameTIME, GameSTART, GameInfo, GameFertilizePlant, GamePlayGame, GameStartGainMaterial, GameStartTimeGainEvent
import pprint
from game_actors_and_handlers.gifts import GiftReceiverBot, AddGiftEventHandler, CakesReceiverBot
from game_actors_and_handlers.plants import HarvesterBot, SeederBot, PlantEventHandler, GameSeedReader,FertilBot
from game_actors_and_handlers.roulettes import RouletteRoller, GameResultHandler, FrutRouletteRoller
from game_actors_and_handlers.wood_graves import WoodPicker, WoodTargetSelecter
from game_actors_and_handlers.cook_graves import BrewPicker, CookerBot, RecipeReader, CookSpeed
from game_actors_and_handlers.digger_graves import BagsPicker, TimeGainEventHandler
from game_actors_and_handlers.stone_graves import StonePicker, StoneTargetSelecter
from game_actors_and_handlers.search_buff import GameBuffDigger
from game_actors_and_handlers.workers import GainMaterialEventHandler
from game_actors_and_handlers.pickups import Pickuper, AddPickupHandler,BoxPickuper, Hoof
from game_actors_and_handlers.location import ChangeLocationBot, GameStateEventHandler
from game_actors_and_handlers.friends import VisitingUsers
from game_state.brains import PlayerBrains
from game_actors_and_handlers.wand import MagicWand
from game_actors_and_handlers.harvest_buff import GameBuffHarvest
from game_actors_and_handlers.friend_dig import FriendDigger
from game_actors_and_handlers.exchange_collection import ExchangeKruger, ExchangeMummy
from game_actors_and_handlers.chop import PirateTreeCut
from game_actors_and_handlers.trade import TraderWork
from game_actors_and_handlers.extra_money import HarvestExchange
from game_actors_and_handlers.building_buyer import BuildingBuyer
#from game_actors_and_handlers.use_egg import UseEggItemBot
#from game_actors_and_handlers.action_user import Action_user
import socket
import urllib2
from game_actors_and_handlers.burrowing import DigBot
from game_actors_and_handlers.storage import SellBot
from game_actors_and_handlers.missions import GetMissionsBot, ViewMissions
from game_actors_and_handlers.rub import Rub
logger = logging.getLogger(__name__)



class GameLocation():

    def __init__(self, item_reader, game_location, game_objects):
        self.__item_reader = item_reader
        self.__game_location = game_location
        self.__game_objects = game_objects
        self.__pickups = []

    def append_object(self, obj):
        self.get_game_objects().append(obj)

    def get_game_location(self):
        return self.__game_location

    def get_game_objects(self):
        #open("game_location.txt","w").write(str(obj2dict(self.get_game_location())))
        #return self.get_game_location().gameObjects
        return self.__game_objects

    def get_location_id(self):
        return self.__game_location.id

    def get_all_objects_by_types(self, object_types):
        objects = []
        for game_object in self.get_game_objects():
            item = self.__item_reader.get(game_object.item)
            if game_object.type in object_types or item.type in object_types:
                objects.append(game_object)
        return objects

    def get_all_objects_by_type(self, object_type):
        return self.get_all_objects_by_types([object_type])

    def get_object_by_id(self, obj_id):
        for game_object in self.get_game_objects():
            if game_object.id == obj_id:
                return game_object
        return None

    def log_game_objects(self):
        for gameObject in self.get_game_objects():
            # if gameObject.type != 'base':
                logger.info(obj2dict(gameObject))

    def remove_object_by_id(self, obj_id):
        for game_object in list(self.get_game_objects()):
            if game_object.id == obj_id:
                self.get_game_objects().remove(game_object)

    def get_pickups(self):
        return tuple(self.__pickups)

    def add_pickups(self, pickups):
        self.__pickups += pickups

    def remove_pickup(self, pickup):
        self.__pickups.remove(pickup)


class GameTimer(object):

    def __init__(self):
        self._client_time = 0
        self._start_time = 0

    def _get_client_time(self):
        random.seed()
        self._client_time = long(random.randrange(2800, 4000))
        self._start_time = time.time()
        return self._client_time

    def _get_current_client_time(self):
        '''
        returns the current in-game time (in milliseconds)
        '''
        currentTime = self._client_time
        currentTime += (time.time() - self._start_time) * 1000
        return currentTime

    def _add_sending_time(self, sending_time):
        self._client_time += sending_time

    def has_elapsed(self, time):
        return int(time) <= self._get_current_client_time()


class GameEventsSender(object):
    def __init__(self, request_sender):
        self.__events_to_handle = []
        self.__request_sender = request_sender

    def print_game_events(self):
        if len(self.__events_to_handle) > 0:
            logger.debug("received events: %s" % self.__events_to_handle)

    def get_game_events(self):
        return list(self.__events_to_handle)

    def send_game_events(self, events=[]):
        '''
        Returns key (string) and time (int)
        '''
        if len(events) > 0:
            logger.debug("events to send: %s" % events)
        command = GameEVT(events=events)
        game_response = self.__request_sender.send(command)
        self.__events_to_handle += game_response.events

    def remove_game_event(self, event):
        self.__events_to_handle.remove(event)


class GameInitializer():
    def __init__(self, timer, site):
        self.__timer = timer
        self.__site = site

    def create_events_sender(self):
        return GameEventsSender(self.__request_sender)

    def start(self):
        logger.info('Загружаем Локацию...')
        # send TIME request (http://java.shadowlands.ru/zombievk/go)
        # handle redirect (save new url: http://95.163.80.20/zombievk)
        # parse auth key and time id
        session_key, server_time = self.get_time()

        # send START
        start_response, friendsid = self.start_game(server_time, session_key)
        logger.info('Локация загружена!')
        return start_response, friendsid, server_time

    def get_time(self):
        '''
        Returns key (string) and time (int)
        '''
        self.__request_sender = self.__create_request_sender()
        key = self.__site.get_time_key()
        command = GameTIME(key=key)
        response = self.__request_sender.send(command)
        return response.key, response.time

    def __create_request_sender(self):
        api_user_id, game_auth_key, api_access_token, connection = self.__site.get_game_params()
        self.__api_access_token = api_access_token
        self.__connection = connection
        self.__session = Session(api_user_id, game_auth_key,
                                 client_version=Game.CLIENT_VERSION)
        factory = message_factory.Factory(self.__session, None)
        request_sender = RequestSender(factory,
                                       self.__connection)
        self.__factory = factory
        return request_sender

    def start_game(self, server_time, session_key):
        self.__factory.setRequestId(server_time)
        self.__factory.setSessionKey(session_key)
        client_time = self.__timer._get_client_time()
        start_time = time.time()
        #print client_time, start_time
        command, friendsid = self.__site.create_start_command(server_time, client_time)
        sending_time = (time.time() - start_time) * 1000
        self.__timer._add_sending_time(sending_time)
        return self.__request_sender.send(command),friendsid

    def _getUserInfo(self):
        '''
        returns user info using vk api
        '''
        # get vk user info
        api = vkontakte.api.API(token=self.__api_access_token)
        info = api.getProfiles(
            uids=self.__session.getUserId(), format='json',
            fields='bdate,sex,first_name,last_name,city,country')
        info = info[0]
        if 'bdate' in info:
            bdate = info['bdate']
        else:
            bdate = None
        my_country = api.places.getCountryById(cids=int(info['country']))[0]
        info['country'] = my_country['name']
        my_city = api.places.getCityById(cids=int(info['city']))[0]
        info['city'] = my_city['name']
        game_info = GameInfo(city=info['city'], first_name=info['first_name'],
                 last_name=info['last_name'],
                 uid=long(info['uid']), country=info['country'],
                 sex=long(info['sex']), bdate=bdate)
        return game_info


class GameState():
    #print dir(self)

    def __init__(self, start_response, item_reader):
        self.__item_reader = item_reader
        self.__game_state = start_response.state


        game_state_event = start_response.params.event
        open('event.txt','w').write(str(obj2dict(game_state_event)))
        #print 'game_state_event-----',obj2dict(game_state_event)

        self.set_game_loc(game_state_event)
        open('stats.txt','w').write(str(obj2dict(self.__game_state)))
        open('dirstate.txt','w').write(str(dir(self.__game_state)))
        #print obj2dict(self.__game_state.location.storageItems)
        print self.__game_state.location.id
        '''self.__player_brains = PlayerBrains(self.__game_state,
                                            self.get_game_loc(),
                                            item_reader)
        total_brain_count = self.__player_brains.get_total_brains_count()
        occupied_brain_count = self.__player_brains.get_occupied_brains_count()
        logger.info("")
        logger.info("Мозги: %d/%d" % (occupied_brain_count, total_brain_count))
        x=0
        z=0
        for burySlot in self.__game_state.burySlots:
            x+=1
            if (hasattr(burySlot, u"user") is True): z+=1
        logger.info("Использование слотов для закопки друзей: %d/%d" % (z,x))
        if len(self.__game_state.buyedBrains)<>0:
          logger.info("Купленные:")
          x=1
          for buyed_brain in self.__game_state.buyedBrains:
              ms=int(buyed_brain.endTime)-((int(buyed_brain.endTime)/1000)*1000)
              s=(int(buyed_brain.endTime)/1000)-(((int(buyed_brain.endTime)/1000)/60)*60)
              m=((int(buyed_brain.endTime)/1000)/60)-((((int(buyed_brain.endTime)/1000)/60)/60)*60)
              h=((int(buyed_brain.endTime)/1000)/60)/60
              logger.info("%d. Время окончания: %d:%d:%d.%d"%(x,h,m,s,ms))
              x+=1'''
        logger.info("")
        logger.info("Уровень: "+str(self.__game_state.level))
        s=''
        for i in range(len(str(self.__game_state.gameMoney)),0,-3):
          if i>=3: s=str(self.__game_state.gameMoney)[i-3:i]+'.'+s
          else: s=str(self.__game_state.gameMoney)[:i]+'.'+s
        logger.info("Монеты: "+s[:-1])
        logger.info("Изумруды: "+str(self.__game_state.cashMoney))
        logger.info("Энергия: "+str(self.__game_state.energy))
        print self.__game_state.cashMoney


    def set_game_loc(self, game_state_event):
        self.__game_loc = GameLocation(self.__item_reader,game_state_event.location,game_state_event.gameObjects)
        for attr, val in game_state_event.__dict__.iteritems():
            self.__game_state.__setattr__(attr, val)
            #print attr
        #self.get_game_loc().log_game_objects()

    def get_location_id(self):
        return self.get_state().locationId

    def get_game_loc(self):
        #print obj2dict(self.__game_loc)
        return self.__game_loc

    def get_state(self):
        #print obj2dict(self.__game_state)
        return self.__game_state

    def get_brains(self):
        return False#self.__player_brains

    def has_in_storage(self, item_id, count):
        for itemid in self.__game_state.location.storageItems:
            if hasattr(itemid, "item"): 
                if itemid.item == item_id:
                    return itemid.count >= count
        return False

    def count_in_storage(self, item_id):
        for itemid in self.__game_state.location.storageItems:
            if hasattr(itemid, "item"): 
                if itemid.item == item_id:
                    return itemid.count
        return 0

    def remove_from_storage(self, item_id, count):
        for itemid in self.__game_state.location.storageItems:
            if hasattr(itemid, "item"): 
                if itemid.item == item_id:
                    itemid.count -= count
                    return True
        return False

    def add_from_storage(self, item_id, count):
        item_id = item_id.lstrip('@')
        item_id = '@'+item_id
        for itemid in self.__game_state.location.storageItems:
            if hasattr(itemid, "item"):
                if itemid.item == item_id:
                    itemid.count += count
                    return
        for itemid in self.__game_state.location.storageGameObjects:
            if hasattr(itemid, "item"):
                if itemid.item == item_id:
                    itemid.count += count
                    return
        self.set_from_storage(item_id, count)
    def set_from_storage(self, item_id, count):
        itemid=dict2obj({u'item': item_id,u'count': count})
        self.__game_state.location.storageItems.append(itemid)
        self.__game_state.location.storageGameObjects.append(itemid)


class Game():

    #CLIENT_VERSION = long(1362084734)
    #CLIENT_VERSION = long(1378103895)
    CLIENT_VERSION = long(1406698583)

    def __init__(self, site, settings,
                 user_prompt, game_item_reader=None, gui_input=None):
        logger.info('Логинимся...')

        self.__timer = GameTimer()
        self.__game_initializer = GameInitializer(self.__timer, site)
        self.__settings = settings

        self.__itemReader = game_item_reader
        self.__user_prompt = user_prompt
        self.__selected_seed = None
        self.__selected_recipe = None
        self.__selected_location = None
        self.__receive_gifts_with_messages = True
        self.__receive_non_free_gifts = True
        self.__gui_input = gui_input
        
        # load settings
        self.__ignore_errors = settings.get_ignore_errors()
        self.__selected_recipe = settings.getUserCook()
        self.__selected_seed = settings.getUserSeed()
        self.__selected_sell = settings.getUserSell()
        self.__selected_send = settings.getUserSend()
        self.__setting_view = settings.GetUserView()
        self.__selected_loc_setting = settings.getUserLoc()
        
        print ''
        if self.__selected_seed<>None: 
            if  (self.__selected_seed=='None'): print u'Выбранные семена: ничего не сажать'
            else:
                if type(self.__selected_seed)==type(''): print u'Выбранные семена: везде "%s"'%str(self.__selected_seed)
                else: 
                    print u'Выбранные семена (остров - семена):'
                    for loc in self.__selected_seed.keys(): 
                        if len(loc)>6: print u'\t%s\t-\t"%s"'%(str(loc),str(self.__selected_seed[loc]))
                        else: print u'\t%s\t\t-\t"%s"'%(str(loc),str(self.__selected_seed[loc]))
        print ''
        if self.__selected_recipe<>None: 
            if  (self.__selected_recipe=='None'): print u'Выбранные рецепты: ничего не варить'
            else:
                if type(self.__selected_recipe)==type(''): print u'Выбранные рецепты: везде "%s"'%str(self.__selected_recipe)
                elif type(self.__selected_recipe)==type([]): print u'Выбранные рецепты: везде "%s"'%str(', '.join(self.__selected_recipe))
                else: 
                    print u'Выбранные семена (остров - рецепт):'
                    for loc in self.__selected_recipe.keys(): 
                        if len(loc)>6: print u'\t%s\t-\t"%s"'%(str(loc),str(self.__selected_recipe[loc]))
                        else: print u'\t%s\t\t-\t"%s"'%(str(loc),str(self.__selected_recipe[loc]))
        if  (self.__selected_sell==None): print u'Предметы на продажу: ничего не продавать'
        else:
            print u'Предметы на продажу (предмет - сколько оставить):'
            for item in self.__selected_sell.keys(): 
                print u'\t"%s"\t\t-\t%s'%(str(item),str(self.__selected_sell[item]))
        print ''
        print u'Настройки показа:'
        if  (self.__setting_view['pickup']): print u'\tПоказывать подбираемые предметы'
        else:  print u'\tНе показывать подбираемые предметы'
        if  (self.__setting_view['location_send']): print u'\tПоказывать перешедшую локацию'
        else:  print u'\tНе показывать перешедшую локацию'
        print ''

    def select_item(self, reader_class, prompt_string):
        item_reader = reader_class(self.__itemReader)
        available_items = item_reader.get_avail_names(self.__game_state_)
        item_name = self.__user_prompt.prompt_user(prompt_string,
                                                   available_items)
        return item_reader.get_by_name(item_name)

    def select_plant_seed(self):
        if self.__selected_seed is None:
            self.__selected_seed = self.select_item(GameSeedReader,
                                                    u'Семена для грядок:')

    def select_recipe(self):
        if self.__selected_recipe is None:
            self.__selected_recipe = self.select_item(RecipeReader,
                                                      u'Рецепт для поваров:')

    def select_location(self):
        #print dir(self)
        #logger.info('Доступные локации:')
        #logger.info('(+ платный, - бесплатный, ? - пещера)')
        locations_nfree = [u'isle_01', 'isle_small', 'isle_star', 'isle_large', 'isle_moon', 'isle_giant', 'isle_xxl', 'isle_desert']
        locations_nwalk = [u'un_0'+str(x+1) for x in range(9)]
        loc_name=self.__itemReader.get(self.get_game_state().location.id).name
        logger.info(u'Текущая локация "%s" '%loc_name.upper())
        #print u'Находимся на локации "%s" '%loc_name.upper()
        locations = {}
        for location in self.get_game_state().locationInfos:
            name = self.__itemReader.get(location.locationId).name
            if (location.locationId not in locations_nfree) and (location.locationId not in locations_nwalk):
                locations[name] = location
                logger.info('\t-\t'+location.locationId+'\t'+name)
            else:
                if (location.locationId not in locations_nfree):
                    logger.info('\t?\t'+location.locationId+'\t'+name)
                else:
                    logger.info('\t+\t'+location.locationId+'\t'+name)
        if locations:
            logger.info('Находимся на острове:')
            #logger.info('   *       '+self.__itemReader.get(self.get_game_loc().get_location_id()).title)
            logger.info("")
            #location_name = self.__user_prompt.prompt_user(u'Выберите остров:',locations.keys())
            location_name = locations.keys()[0]
            if location_name in locations:
                self.__selected_location  = locations[location_name].locationId
            else:
                self.__selected_location  = self.get_game_loc().get_location_id()

    def get_user_setting(self, setting_id):
        return self.__settings.get


    def running(self):
        if self.__gui_input:
            running = self.__gui_input.running
        else:
            running = lambda: True
        return running()

    def start(self):

        while(self.running()):
            try:
                # load items dictionary
                if self.__itemReader is None:
                    logger.info('Загружаем словарь объектов...')
                    item_reader = GameItemReader()
                    item_reader.download('items.txt')
                    item_reader.read('items.txt')
                    self.__itemReader = item_reader
                    logger.info('Словарь объектов загружен')
                start_response,self.__friendsid,self.__server_time = self.__game_initializer.start()
                # Save Game_state
                #open("game_state.txt","w").write(str(obj2dict(start_response)))
                
                self.__game_events_sender = self.__game_initializer.create_events_sender()

                self.save_game_state(start_response)
                
#                GetMissionsBot(self.__itemReader, self.__game_state_, self.__game_events_sender, self._get_timer(),{}).perform_action()
                
                self.select_location()

                self.select_plant_seed()
                
                self.select_recipe()
                
                self.create_all_actors()

                # TODO send getMissions
                # TODO handle getMissions response

                self.eventLoop()
            except urllib2.HTTPError, e:
                raise e
            except (socket.timeout, urllib2.HTTPError, urllib2.URLError):
                seconds = 5
                logger.error('Timeout occurred, retrying in %s seconds...'
                             % seconds)
                time.sleep(seconds)
            except (socket.error, ssl.SSLError) as e:
                seconds = 15
                logger.error('Socket error occurred, retrying in %s seconds...'
                             % seconds)
                time.sleep(seconds)
            except message_factory.GameError, e:
                if not self.__ignore_errors:
                    raise e

    def save_game_state(self, start_response):
        # parse game state
        self.__game_state_ = GameState(start_response, self.__itemReader)

    def get_game_loc(self):
        return self.__game_state_.get_game_loc()

    def get_game_state(self):
        return self.__game_state_.get_state()

    def eventLoop(self):
        '''
        in a loop, every 30 seconds
        send EVT request
        handle EVT response
        '''
        interval = 5
        refresh_min = 5
        seconds = interval
        ref_min = []
        while(self.running()):
            if seconds >= interval:
                self.perform_all_actions()
                #logger.info('Ждем %d секунд'%interval)
                seconds = 0
            time.sleep(0.1)
            seconds += 0.1
            
            cur_time = self.__timer._get_current_client_time()
            min = int(int(cur_time/1000)/60)
            if min not in ref_min:
                if (refresh_min-min)==1: logger.info(u'Перезагрузка через %s минуту'%str(refresh_min-min))
                elif ((refresh_min-min)>=2) and ((refresh_min-min)<=4): logger.info(u'Перезагрузка через %s минуты'%str(refresh_min-min))
                else: logger.info(u'Перезагрузка через %s минут'%str(refresh_min-min))
                ref_min += [min]
            if min>=refresh_min: 
                ref_min = []
                break

    def create_all_actors(self):
        receive_options = {'with_messages': self.__receive_gifts_with_messages,
                           'non_free': self.__receive_non_free_gifts}
        options = {'GiftReceiverBot': receive_options,
                   'SeederBot': self.__selected_seed,
                   'CookerBot': self.__selected_recipe,
                   'ChangeLocationBot': self.__selected_location,
                   'VisitingUsers':self.__friendsid,
                   'DigBot':self.__friendsid,
                   'SellBot':{'sell_item':self.__selected_sell,'send_user':self.__selected_send},
                   'ChangeLocationBot':self.__selected_loc_setting,
                  }
        events_sender = self.__game_events_sender
        timer = self._get_timer()
        item_reader = self.__itemReader
        game_state = self.__game_state_
        actor_classes = [
            #FriendDigger,        #Компаем у друзей
            #DigBot,             # Работа с мозгами
            #GetMissionsBot,     # Запрос выполнения миссий
            #VisitingUsers,      # Посещение друзей
            #GameBuffHarvest, #Приём супер урожая
            #GameBuffDigger,     # Приём супер-поиск
            WoodPicker,         # Сбор дерева
            StonePicker,        # Сбор камня
            #BrewPicker,         # Сбор сваренного
            BagsPicker,         # Сбор сумок
            #WoodTargetSelecter, # Отправка работать дровосекам
            #StoneTargetSelecter,# Отправка работать камнетёсов
            #CookerBot,          # Работа с поварами (подъем из могил, установка рецептов)
            #CookSpeed,          # Посолить рецепты
            #FertilBot,          # Удобрение деревьев
            HarvesterBot,       # Сбор чего либо + вскапывание грядок
            #CakesReceiverBot,   # Сбор пряников
            SeederBot,          # Посейка
            GiftReceiverBot,    # Принятие подарков
            BoxPickuper,        # Вскрытие чего либо
            RouletteRoller,     # Кручение рулеток
            #FrutRouletteRoller, # Кручение фруктовых рулеток
            #UseEggItemBot,      # Бить яйца ;)
            #MagicWand,          # Добыча ресурсов палочками
            #ExchangeKruger,      # Создаем коллекцию фреди в изумрудной мельнице
            #ExchangeMummy,       # Создаем коллекцию мумии в изумрдуном маяке
            Pickuper,           # Сбор дропа
            SellBot,            # Продажа чего либо
            #TraderWork,         # Торговцы
            #BuildingBuyer,     # Покупаем, продаем ракету
            #HarvestExchange,    #создаем деньги в БЦ
            #PirateTreeCut,     #рубка на острове сокровищ
            #ChangeLocationBot,  # Переход по локациям
            #Action_user, # Действия игрока
            Hoof,
            Rub,
        ]
        self.__actors = []
        for actor_class in actor_classes:
            self.__actors.append(
                actor_class(item_reader, game_state, events_sender, timer,
                            options))

    def perform_all_actions(self):
        '''
        Assumes that create_all_actors is called before
        '''
        #all_time=[]
        game_state = self.__game_state_
        for actor in self.__actors:
            #time_one=time.time()
            actor.perform_action()
            #time_two=time.time()
            #logger.info(u'Класс %s' % (str(actor).split()[0].split('.')[-1]))
            #logger.info(u'Выполнялся %f' % (time_two-time_one))
            #all_time+=[[str(actor).split()[0].split('.')[-1],(time_two-time_one)]]
            self.handle_all_events()
        #open('time.txt','a').write(str(all_time))
        self.__game_events_sender.send_game_events()
        self.handle_all_events()
        #raw_input()


    def handle_all_events(self):
        self.__game_events_sender.print_game_events()
        for event in self.__game_events_sender.get_game_events():
            self.handleEvent(event)

    def handleEvent(self, event_to_handle):
        if event_to_handle.action == 'addGift':
            AddGiftEventHandler(self.get_game_state()).handle(event_to_handle)
        elif event_to_handle.action == 'add':
            if event_to_handle.type == 'pickup':
                AddPickupHandler(self.__itemReader, self.get_game_loc(),self.__game_state_,self.__setting_view).handle(event_to_handle)
        elif event_to_handle.type == GameFertilizePlant.type:
            PlantEventHandler(self.get_game_loc()).handle(event_to_handle)
        elif event_to_handle.type == GamePlayGame.type:
            GameResultHandler(self.__itemReader,self.get_game_loc(),self.__game_state_).handle(event_to_handle)
        elif event_to_handle.type == GameStartGainMaterial.type:
            GainMaterialEventHandler(self.__itemReader, self.get_game_loc(),
                                     self.__timer).handle(event_to_handle)
        elif event_to_handle.type == GameStartTimeGainEvent.type:
            TimeGainEventHandler(self.__itemReader, self.get_game_loc(),
                                 self.__timer).handle(event_to_handle)
        elif event_to_handle.type == 'gameState':
            GameStateEventHandler(self.__game_state_, self.__server_time,self.__setting_view).handle(event_to_handle)
        elif event_to_handle.type == 'mission':
            ViewMissions(self.__itemReader, self.__setting_view).handle(event_to_handle)
        else:
            self.logUnknownEvent(event_to_handle)
        self.__game_events_sender.remove_game_event(event_to_handle)

    def logUnknownEvent(self, event_to_handle):
        logger = logging.getLogger('unknownEventLogger')
        logger.info(pprint.pformat(obj2dict(event_to_handle)))

    def _get_timer(self):
        return self.__timer

    def get_request_sender(self):
        return self.__request_sender


class RequestSender(object):
    def __init__(self, message_factory, connection):
        self.__factory = message_factory
        self.__connection = connection

    def send(self, data):
        data = obj2dict(data)
        assert 'type' in data
        request = self.__factory.createRequest(data)
        return dict2obj(request.send(self.__connection))

    def set_url(self, url):
        self.__connection.setUrl(url)

    def clear_session(self):
        self.__factory.setSessionKey(None)

    def reset_request_id(self):
        request_id = message_factory._getInitialId()
        self.__factory.setRequestId(request_id)

    def set_auth_key(self, auth_key):
        self.__factory.set_auth_key(auth_key)
