# coding=utf-8
import logging
from game_state.game_types import GameCookGrave, GameCookGraveWithBrains, GameCookItem, GameCookSpeed, GameCookStart, GameCookStop
from game_state.item_reader import LogicalItemReader
from game_actors_and_handlers.workers import ResourcePicker, TargetSelecter
from game_state.game_event import obj2dict
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class BrewPicker(ResourcePicker):

    def get_worker_types(self):
        return [GameCookGrave.type, GameCookGraveWithBrains.type]
        
class CookSpeed(BaseActor):

    def get_worker_types(self):
        return [GameCookGrave.type, GameCookGraveWithBrains.type]
  
    def perform_action(self):
        wood_graves = self._get_game_location().get_all_objects_by_types(
            self.get_worker_types()
        )
        recipe_item = {u'@RECIPE_31',u'@RECIPE_53'}
        speed_item = 'RED_SPEEDUPER'
        if self._get_game_state().count_in_storage('@'+speed_item)>0:
            for wood_grave in wood_graves:
                #print obj2dict(wood_grave)
                #{u'rotate': 0L, u'jobEndTime': u'2258993', u'speeduped': False, u'id': 3620L, u'materials': [], u'item': u'@SC_COOK_GRAVE', u'isUp': True, u'recipeNo': 360L, u'y': 35L, u'x': 21L, u'type': u'cookGrave', u'pendingRecipes': [u'@RECIPE_09', u'@RECIPE_09'], u'currentRecipe': u'@RECIPE_09'}
                if hasattr(wood_grave, "isUp") or wood_grave.isUp:
                    if hasattr(wood_grave, "currentRecipe"):
                        count_speed=0
                        if wood_grave.currentRecipe in recipe_item: count_speed+=1
                        for i in wood_grave.pendingRecipes:
                            if i in recipe_item: count_speed+=1
                            else: break
                        if count_speed==0: break
                        logger.info(u'Посолим %d рецепта у поваров №%d'%(count_speed,wood_grave.id))
                        for i in range(count_speed):
                            if self._get_game_state().count_in_storage('@'+speed_item)>0:
                                #{"objId":3494,"type":"item","action":"speedup","itemId":"RED_SPEEDUPER"}
                                event=GameCookSpeed(objId=wood_grave.id,itemId=unicode(speed_item))
                                self._get_events_sender().send_game_events([event])
                                self._get_game_state().remove_from_storage('@'+speed_item,1)
                            else: break

class CookerBot(TargetSelecter):
    MAX_PENDING_RECIPES = 2

    def get_worker_types(self):
        return [GameCookGrave.type, GameCookGraveWithBrains.type]
        
    def perform_action(self):
        wood_graves = self._get_game_location().get_all_objects_by_types(
            self.get_worker_types()
        )
        free_workers = []
        for wood_grave in wood_graves:
            if self.is_busy(wood_grave):
                free_workers.append(wood_grave)
        for free_worker in free_workers:
            self.start_job(free_worker)

    def is_busy(self, worker):
        return (not self._get_player_brains().is_using_brains(worker)) or (self.free_pendig(worker)>0)
    
    def free_pendig(self, free_worker):
        empty_buckets = CookerBot.MAX_PENDING_RECIPES - len(free_worker.pendingRecipes)
        if (hasattr(free_worker, "currentRecipe") is False): empty_buckets+=1
        return empty_buckets

    def start_job(self, free_worker):
        cook_items = self._get_options()
        if (cook_items<>None) and (cook_items<>'None'):
            location = self._get_game_state().get_game_loc().get_location_id()
            
            cur_rec=-1
            if type(cook_items)==type(''): cook_item = self._get_item_reader().get(cook_items)
            elif type(cook_items)==type({}):
                if location in cook_items.keys(): cook_id = cook_items[location]
                else: cook_id = cook_items['other']
                if cook_id=='None': return
                cook_item = self._get_item_reader().get(cook_id)
            elif type(cook_items)==type([]): 
                cur_rec = 0
                cook_item = self._get_item_reader().get(cook_items[cur_rec])
            else: cook_item=cook_items
            
            if self._get_player_brains().has_sufficient_brains_count(free_worker):
                if not hasattr(free_worker, "isUp") or not free_worker.isUp:
                    logger.info(u'Повара отдыхают запустим работать №'+str(free_worker.id))
                    start_item_event = GameCookStart(free_worker.id)
                    self._get_events_sender().send_game_events([start_item_event])
                    free_worker.isUp = True
                
            empty_buckets = self.free_pendig(free_worker)
            if cur_rec==-1:
                for _ in range(empty_buckets):
                    if self.has_enough_ingredients(cook_item.ingridients):
                        self.fill_basket(free_worker, cook_item)
                        self.remove_ingredients(cook_item.ingridients)
            else:
                while (empty_buckets<>0):
                    for _ in range(empty_buckets):
                        if self.has_enough_ingredients(cook_item.ingridients):
                            self.fill_basket(free_worker, cook_item)
                            self.remove_ingredients(cook_item.ingridients)
                            empty_buckets -= 1
                    if (cur_rec<>len(cook_items)-1): cur_rec += 1
                    cook_item = self._get_item_reader().get(cook_items[cur_rec])
            

    def has_enough_ingredients(self, ingredients):
        for ingredient in ingredients:
            if not self._get_game_state().has_in_storage(ingredient.item,
                                                        ingredient.count):
                return False
        return True

    def remove_ingredients(self, ingredients):
        for ingredient in ingredients:
            self._get_game_state().remove_from_storage(ingredient.item,
                                                       ingredient.count)

    def fill_basket(self, free_worker, cook_item):
        logger.info(u'Добавляем рецепт "%s" поварам №%d' %(cook_item.name,free_worker.id))
        cook_item_event = GameCookItem(cook_item.id,free_worker.id)
        self._get_events_sender().send_game_events([cook_item_event])
        if not self.has_current_recipe(free_worker):
            free_worker.currentRecipe = cook_item.id
        else:
            free_worker.pendingRecipes.append(cook_item.id)

    def has_current_recipe(self, free_worker):
        return hasattr(free_worker, "currentRecipe") and free_worker.currentRecipe


class RecipeReader(LogicalItemReader):
    def __init__(self, game_item_reader):
        self._item_reader = game_item_reader

    def _get_item_type(self):
        return 'recipe'

    def _get_all_item_ids(self):
        return self._item_reader.get('recipes').items


# TODO cooker event: set isUp to False, currentRecipe to the next pending recipe
