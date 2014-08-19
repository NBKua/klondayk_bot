#coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict
logger = logging.getLogger(__name__)

class DeletingObjects(BaseActor):
    def perform_action(self):
        obj_del = ''   
        type_del = ''
        
        # Выбираем, что удалять
        obj_del = '@P_27' # object.item   
        #type_del = 'decoration' # object.type
        
        # На каком острове
        loc_del = [
                #'main',                # Домашний
                #'isle_03',             # Любви
                #'isle_02',             # Майя
                #'isle_x',              # X
                #'isle_faith',          # Веры
                #'isle_hope',           # Надежды
                #'isle_scary',          # Страшный
                #'isle_alpha',          # Альфа
                #'isle_omega',          # Омега
                #'isle_sand',           # Песочный
                #'isle_polar',          # Полярной ночи
                #'isle_wild',           # Дремучий
                'isle_mobile',         # Мобильный
                #'isle_ufo',            # НЛО
                #'isle_dream',          # Мечты
                #'isle_scarecrow',      # Пик Админа
                #'isle_elephant',       # Ужасный
                #'isle_emerald',        # Город Призрак
                #'isle_monster',        # Чудовища
                #'isle_halloween',      # Лысая гора
                #'isle_light',          # Вишневый 
                #
                ###############     Платные     ###############
                #
                #'isle_01',             # Секретный
                #'isle_small',          # Маленькой ёлочки
                #'isle_star',           # Звездный
                #'isle_large',          # Большой ёлки
                #'isle_moon',           # Лунный
                #'isle_giant',          # Гигантов
                #'isle_xxl',            # Огромной ёлки
                #'isle_desert'          # Необитаемый
                ]
                
        current_loc = self._get_game_state().get_location_id()        
        if not current_loc in loc_del:
            #logger.info(u"Пропускаем "+current_loc)
            return 1
        count_del = 0
        for object in self._get_game_location().get_game_objects():
            if object.type == type_del:
                self._get_events_sender().send_game_events([{"type":"item","objId":object.id,"action":"sell"}])
                #self._get_game_location().remove_object_by_id(object.id)
                count_del += 1
            if object.item == obj_del:
                self._get_events_sender().send_game_events([{"type":"item","objId":object.id,"action":"sell"}])
                #self._get_game_location().remove_object_by_id(object.id)
                count_del += 1
        if count_del > 0:
            logger.info(u'Удалили %d объекта(ов)' % str(count_del))