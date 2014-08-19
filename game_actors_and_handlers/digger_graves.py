# coding=utf-8
import logging
from game_state.game_types import GameDiggerGrave, GameDiggerGraveWithBrains,\
    GamePickItem, GameGainItem, GamePickup
from game_actors_and_handlers.workers import ResourcePicker


logger = logging.getLogger(__name__)

class BagsPicker(ResourcePicker):

    def get_worker_types(self):
        return [GameDiggerGrave.type, GameDiggerGraveWithBrains.type]
    
    def perform_action(self):
        graves = self._get_game_location().get_all_objects_by_types(self.get_worker_types())
        for grave in graves:

            # Если рыбак не работает
            if not grave.started:

                # Получаем его название
                grave_name = self._get_item_reader().get(grave.item).name
                
                # Выполняем запрос на сервер
                logger.info(u'Выгоняем работать %s %i' % (grave_name, grave.id))
                grave_start_event = {u'type': u'item', u'action': u'start', u'objId': grave.id}
                self._get_events_sender().send_game_events([grave_start_event])

                # Исправляем game_state, чтобы при следующем цикле он не посчитал рыбака не рабочим
                grave.started = True

            # Если есть мешки у рыбака
            if grave.materials == 3:
                logger.info("Собираем мешки " + str(grave.materials) + ' шт.')
                for _ in range(grave.materials):
                    self._pick_material(grave, None)
                    grave.materials -= 1
         
                

class TimeGainEventHandler(object):

    def __init__(self, item_reader, game_location, timer):
        self.__item_reader = item_reader
        self.__game_location = game_location
        self.__timer = timer

    def _get_timer(self):
        return self.__timer

    def handle(self, event_to_handle):
        gameObject = self.__game_location.get_object_by_id(
            event_to_handle.objId
        )
        if gameObject is None:
            logger.critical("OMG! No such object")
            return
        else:
            worker = self.__item_reader.get(gameObject.item).name
            if hasattr(gameObject, 'gainTime') and gameObject.gainTime and self._get_timer().has_elapsed(gameObject.gainTime):
                    logger.info(worker + u' принёс')
                    gameObject.materials += 1
                    gameObject.gainTime = None
            if event_to_handle.action == 'start':
                gameObject.started = True
		if hasattr(event_to_handle,'gainTime'):	
				gameObject.gainTime = event_to_handle.gainTime
				logger.info(worker + u' принесёт через ' + str((int(gameObject.gainTime) - self._get_timer()._get_current_client_time())/1000/60) + u' мин.')
            else:
                gameObject.started = False
