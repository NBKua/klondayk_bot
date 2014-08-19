# coding=utf-8
import logging
from math import ceil
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict


logger = logging.getLogger(__name__)

class ExhangeCollEmerald(BaseActor):

  #функция создания чего-либо
  def create_items (self, _obj_id,_item_id):
    create_items_event = {"type": "item",
                           "action": "craft",
                           "objId": _obj_id,
                           "itemId":_item_id}        
    self.events_append(create_items_event)
    
         
  def events_append(self, event):
    self._events.append(event)
    if len(self._events) > 100:
        self.events_free()

  def events_free(self):
    if self._events != []: self._get_events_sender().send_game_events(self._events)
    self._events = []

  def perform_action(self):

    min_coll = 500   # Оставляем Японской коллекции 

    _loc = self._get_game_state().get_game_loc().get_location_id()                                                      
    if not (_loc == u'isle_02' or _loc == u'isle_elephant'):
        return 1

    self._events = []
                                                   
    if _loc == u'isle_02':
        obj_id_observatory = ''
        #получаем id
        bozon=self._get_game_state().count_in_storage('@CR_666')
        buildings = self._get_game_location().get_all_objects_by_type(GameBuilding.type)
        jap_1=jap_2=jap_3=jap_4=jap_5=0
        for building in list(buildings):
          
            if building.item == '@B_OBSERVATORY':
                obj_id_observatory = building.id
        
        if obj_id_observatory != '' :
          
            cl_items = obj2dict(self._get_game_state().get_state().collectionItems)
            if 'C_36_1' in cl_items.keys():jap_1 = cl_items['C_36_1']   # Японская
            if 'C_36_2' in cl_items.keys():jap_2 = cl_items['C_36_2']   # Японская
            if 'C_36_3' in cl_items.keys():jap_3 = cl_items['C_36_3']   # Японская
            if 'C_36_4' in cl_items.keys():jap_4 = cl_items['C_36_4']   # Японская
            if 'C_36_5' in cl_items.keys():jap_5 = cl_items['C_36_5']   # Японская
            ##### Изумрудка #####
            if obj_id_observatory != '':
              minreal=min(jap_1,jap_2,jap_3,jap_4,jap_5)
              countcol=minreal-min_coll
              needcountbozon=int(round(countcol/10))
              if bozon>needcountbozon:
                if needcountbozon>0:
                  for i in range(needcountbozon):
                    self._get_game_state().remove_from_storage('@CR_666',5)
                    self.create_items(obj_id_observatory, "11")
                    self.create_items(obj_id_observatory, "12")
                    self.create_items(obj_id_observatory, "13")
                    self.create_items(obj_id_observatory, "14")
                    self.create_items(obj_id_observatory, "15")
                  firstcount=(i + 1)*10
                  endcount=(i + 1)*5
                  logger.info(u"Создали %d шт. 'Четвертак"%(endcount))
                  logger.info(u"Создали %d шт. 'Золотой орех"%(endcount))
                  logger.info(u"Создали %d шт. 'Изумруд"%(endcount))
                  logger.info(u"Создали %d шт. 'Кленовый листок"%(endcount))
                  logger.info(u"Создали %d шт. 'Соломинка"%(endcount))
                  cl_items['C_36_1']-=firstcount
                  cl_items['C_36_2']-=firstcount
                  cl_items['C_36_3']-=firstcount
                  cl_items['C_36_4']-=firstcount
                  cl_items['C_36_5']-=firstcount
                  bozon-=needcountbozon
                  if 'C_42_1' in cl_items.keys():cl_items['C_42_1']+= endcount
                  else:cl_items['C_42_1']= endcount
                  if 'C_42_2' in cl_items.keys(): cl_items['C_42_2']+= endcount
                  else:cl_items['C_42_2']= endcount
                  if 'C_42_3' in cl_items.keys():cl_items['C_42_3']+= endcount
                  else:cl_items['C_42_3']= endcount
                  if 'C_42_4' in cl_items.keys():
                    cl_items['C_42_4']+= endcount
                  else:cl_items['C_42_4']= endcount
                  if 'C_42_5' in cl_items.keys():
                    cl_items['C_42_5']+= endcount
                  else:cl_items['C_42_5']= endcount
              #else:print u'Не хватает БОЗОНА'
                  
        self.events_free()
        self._get_game_state().get_state().collectionItems=dict2obj(cl_items)
        return 1

