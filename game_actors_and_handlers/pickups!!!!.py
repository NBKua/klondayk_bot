# coding=utf-8
import logging
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup, GamePirateCapture
from game_actors_and_handlers.base import BaseActor


logger = logging.getLogger(__name__)

 
class Pickuper(BaseActor):

    def perform_action(self):
        pickups = self._get_game_location().get_pickups()
        self.pick_pickups(pickups)

    def pick_pickups(self, pickups):
        if pickups:
            logger.info(u'Подбираем дроп...')
            
        all_pick = []
        for pickup in pickups:
            pick_event = GamePickPickup([pickup])
            all_pick += [pick_event]
        if len(all_pick)>0:
            self._get_events_sender().send_game_events(all_pick)
            for pickup in pickups:
                self._get_game_location().remove_pickup(pickup)
        '''        
        for pickup in pickups:
            pick_event = GamePickPickup([pickup])
            self._get_events_sender().send_game_events([pick_event])
            self._get_game_location().remove_pickup(pickup)'''


class BoxPickuper(BaseActor):

    def getOpeningPriceMsg(self, boxItem):
        openingPrice = boxItem.openingPrice[0]
        count = openingPrice.count
        item_name = self._get_item_reader().get(openingPrice.item).name
        price_msg = u'%d %s' % (count, item_name)
        return price_msg

    def perform_action(self):
        box_all = 0
        boxes = self._get_game_location().get_all_objects_by_type(
                                                    GamePickup.type)      
        pirate_captures = self._get_game_location().get_all_objects_by_type(
                        GamePirateCapture.type)
        
        if pirate_captures:
          
          for pirate_capture in list(pirate_captures):  
            name = self._get_item_reader().get_name(pirate_capture)
            pick_event = {"objId": pirate_capture.id,
                          "type": "pirateCapture",
                          "action":"capture"}      
            logger.info(u'Вскрываем %s' % name)
            self._get_events_sender().send_game_events([pick_event])
            self._get_game_location().remove_object_by_id(pirate_capture.id)
            
        
        for box in boxes:
            name = self._get_item_reader().get_name(box)
            boxItem = self._get_item_reader().get(box.item)
            enemies = self._get_game_location().get_all_objects_by_type("pirateEnemy")
            enemy_here = 0
            if enemies:
                for enemy in enemies:
                    if(((enemy.x - box.x)**2+(enemy.y - box.y)**2)**0.5 < 15):
                        enemy_here = 1
                        break
            if(enemy_here == 1):
                self._get_game_location().remove_object_by_id(box.id)
                print name
                logger.info(u'Сильвер мешает взять ' + name)
                continue
            gain_event = {"type":"pirateCapture","objId":box.id,"action":"capture"}
            print gain_event
            logger.info(u"Открываем " + name)
            pick_event = GamePickItem(objId=box.id)
            self._get_events_sender().send_game_events( [pick_event] )
            self._get_game_location().remove_object_by_id(box.id)



class AddPickupHandler(object):
    def __init__(self, itemReader, game_location, game_state, setting_view):
        self.__game_loc = game_location
        self.__item_reader = itemReader
        self.__game_state_ = game_state
        self.__setting_view = setting_view

    def handle(self, event_to_handle):
        if event_to_handle is None:
            logger.critical("OMG! No such object")
            return
        else:
            tmp={}
            for pickup in event_to_handle.pickups:
                item_type_msg = {
                    'coins':
                        lambda pickup: u'денег',
                    'xp':
                        lambda pickup: u'опыта',
                    'collection':
                        lambda pickup: u'предмет(ов) коллекции ',
                    'storageItem':
                        lambda pickup: u'предмет(ов) ',
                    'shovel':
                        lambda pickup: u'лопат',
                    'scrapItem':
                        lambda pickup: u'шт. металлолома'
                }.get(pickup.type, lambda pickup: pickup.type)(pickup)
                if (pickup.type=='collection') or (pickup.type=='storageItem'):
                    item_type_msg = ('%s%s'%(item_type_msg,self.__item_reader.get(pickup.id).name))
                if item_type_msg in tmp.keys(): tmp[item_type_msg]+=pickup.count
                else: tmp[item_type_msg]=pickup.count
                # Добавление в game_state
                if hasattr(pickup, "id"):
                    self.__game_state_.add_from_storage('@'+pickup.id, pickup.count)
            if self.__setting_view['pickup']:
                if len(tmp.keys())>0:
                    for i in tmp.keys():
                        logger.info(u'Подобрали %d %s' % (tmp[i], i))
            self.__game_loc.add_pickups(event_to_handle.pickups)
            
            
class MonsterPit(BaseActor):

    def perform_action(self):
        monster = self._get_game_location().get_all_objects_by_type('monsterPit')
        if (len(monster) > 0):
            if (monster[0].state == 'HAVE_PICKUP_BOX'):
                monster_event = {
                    'objId': str(monster[0].id),
                    'type': 'item',
                    'action': 'pick'
                    }

                logger.info(u'Забираем сундук монстра...')
                self._get_events_sender().send_game_events([monster_event])

            if (monster[0].state == 'READY_FOR_DIG'):
                monster_event = {
                    'objId': str(monster[0].id),
                    'type': 'item',
                    'action': 'startDig'
                    }
                logger.info(u'Зкапываем монстра...')
                self._get_events_sender().send_game_events([monster_event])            
