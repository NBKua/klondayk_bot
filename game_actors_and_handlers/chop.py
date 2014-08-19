# coding=utf-8
import logging
#import pdb
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)




class PirateTreeCut(BaseActor):

    def get_object_type(self):
        return "chop"


    def perform_action(self):
        resources = self._get_game_location().get_all_objects_by_type(
                    self.get_object_type()
                )
        enemies = self._get_game_location().get_all_objects_by_type("pirateEnemy")

        # пиратские острова : Остров сокровищ , Таинственный , Жуткий , Северный полюс , Остров сокровищ , Древний
        pirate_locs_id = ["exploration_isle1_random","exploration_isle2_random","exploration_isle3_random","exploration_snow1","exploration_isle1_1","exploration_isle4_random"]
        # Не понятно, что это за острова в списке ???? - Пушистый 1,2,3 и Подземелье 1,2
        #"exploration_furry1","exploration_furry2","exploration_furry3","exploration_isle_un1_1","exploration_isle_un1_2"

        instruments = [] # переменная для инструментов

        _loc = self._get_game_state().get_game_loc().get_location_id() # текущая локация
        #print _loc

        if resources:

          if _loc not in pirate_locs_id:
            st_items = self._get_game_state().get_state().storageItems # Предметы на складе
            for item in list(st_items):
              if hasattr(item, "item"):
                if item.item == ('@CHOP_MACHETE'): #мачете
                  instruments.append(dict2obj({"item":"@CHOP_MACHETE", "count": item.count}))
                if item.item == ('@CHOP_AXE'): #топор
                  instruments.append(dict2obj({"item":"@CHOP_AXE", "count": item.count}))
                if item.item == ('@CHOP_HAMMER'): #кирка
                  instruments.append(dict2obj({"item":"@CHOP_HAMMER", "count": item.count}))
          else: instruments = self._get_game_state().get_state().pirate.instruments


          for resource in resources:
            resource_name = self._get_item_reader().get_name(resource)
            #print resource_name
            tool_needed = resource.chopCount
            type_of_res = resource.item
            type_of_instrument = self._get_item_reader().get(type_of_res).chopInstrumentType
            for tool in instruments:
                name_tool = self._get_item_reader().get_name(tool)
                #print name
                #print "self._get_item_reader().get(tool.item).chopInstrumentType", self._get_item_reader().get(tool.item).chopInstrumentType
                #print "type_of_instrument", type_of_instrument

                if self._get_item_reader().get(tool.item).chopInstrumentType == type_of_instrument and tool.count >= tool_needed:
                    enemy_here = 0
                    if enemies:
                        for enemy in enemies:
                            #Заменили квадрат 10x10 на радиус
                            #if((enemy.x - 15 <= resource.x and enemy.x + 15 >= resource.x) or (enemy.y - 15 <= resource.y and enemy.y + 15 >=resource.y)):
                            if(((enemy.x - resource.x)**2+(enemy.y - resource.y)**2)**0.5 < 15):
                                enemy_here = 1
                                break
                    if(enemy_here == 1):
                        self._get_game_location().remove_object_by_id(resource.id)
                        logger.info(u"Сильвер мешает вырубке " + resource_name)
                        #logger.info(u"Сильвер мешает вырубке "+ name)
                        break
                    #print tool.count, tool_needed
                    gain_event = {"type":"chop","objId":resource.id,"instruments":{self._get_item_reader().get(tool.item).id:tool_needed},"action":"chop"}
                    #print gain_event
                    #logger.info("Рубим с помощью " + str(type_of_instrument))
                    logger.info(u"Рубим " + resource_name + u" с помощью " + str(tool_needed) + u" " + name_tool)
                    self._get_events_sender().send_game_events( [gain_event] )
                    self._get_game_location().remove_object_by_id(resource.id)
                    tool.count -= tool_needed
                    break
        else:
            logger.info("Не осталось ресурсов для добычи")
        resources = self._get_game_location().get_all_objects_by_type("pirateCaptureObject")
        if resources:
            for resource in resources:
                resource_name = self._get_item_reader().get_name(resource)
                enemy_here = 0
                if enemies:
                    for enemy in enemies:
                        #Заменили квадрат 10x10 на радиус
                        #if((enemy.x - 15 <= resource.x and enemy.x + 15 >= resource.x) or (enemy.y - 15 <= resource.y and enemy.y + 15 >= resource.y)):
                        if(((enemy.x - resource.x)**2+(enemy.y - resource.y)**2)**0.5 < 15):
                            enemy_here = 1
                            break
                if(enemy_here == 1):
                    self._get_game_location().remove_object_by_id(resource.id)
                    #logger.info("Сильвер мешает взять "+str(resource.id))
                    logger.info(u"Сильвер мешает взять " + resource_name)
                    continue
                gain_event = {"type":"pirateCapture","objId":resource.id,"action":"capture"}
                #print gain_event
                #logger.info("Открываем " + str(resource.id))
                logger.info(u"Открываем " + resource_name)
                self._get_events_sender().send_game_events( [gain_event] )
                self._get_game_location().remove_object_by_id(resource.id)
        else:
            logger.info("Нет неоткрытых сокровищ")