# coding=utf-8
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup,\
     GameTraderGrave, GameTraderGraveWithBrains
from game_state.game_event import dict2obj
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class TargetSelecter(BaseActor):

    def get_worker_types(self):
        return []

    def get_object_type(self):
        return None

    def get_sent_job(self):
        return ""

    def is_busy(self, worker):
        return self._get_player_brains().is_using_brains(worker)

    def perform_action(self):
        # get all free workers
        wood_graves = self._get_game_location().get_all_objects_by_types(
            self.get_worker_types()
        )
        # get free workers
        free_workers = []
        for wood_grave in wood_graves:
            if not self.is_busy(wood_grave):
                free_workers.append(wood_grave)
        # for each free worker
        for free_worker in free_workers:
            # check brains count
            if self._get_player_brains().has_sufficient_brains_count(
                                                                free_worker):
                self.start_job(free_worker)

    def start_job(self, free_worker):
        logger.info("Отправляем зомби на работу")
        # select any wood tree
        resources = self._get_game_location().get_all_objects_by_type(
            self.get_object_type()
        )
        if resources:
             # make sure gain is not started yet
             resource = self.__find_first_gain_not_started(resources)
             if not resource:
                 logger.info("Все ресурсы уже добываются")
             else:
                 logger.info(self.get_sent_job())
                 gain_event = GameGainItem(resource.id, free_worker.id)
                 self._get_events_sender().send_game_events(
                                                     [gain_event])
                 resource.gainStarted = True
        else:
            logger.info("Не осталось ресурсов для добычи")

    def __find_first_gain_not_started(self, resources):
        for resource in resources:
            if not resource.gainStarted:
                return resource


class ResourcePicker(BaseActor):

    def get_worker_types(self):
        return []

    def perform_action(self):
        wood_graves = self._get_game_location().get_all_objects_by_types(
                            self.get_worker_types())
        for wood_grave in wood_graves:
            for material_id in list(wood_grave.materials):
                material = self._get_item_reader().get(material_id)
                name = material.name
                logger.info(u'Подбираем ' + name)
                self._pick_material(wood_grave, material.id)
                # update game state
                if material.id<>None: self._get_game_state().add_from_storage('@'+material.id,1)
                wood_grave.materials.remove(material_id)

    def _pick_material(self, wood_grave, material_id):
        pick_item = GamePickItem(itemId=material_id, objId=wood_grave.id)
        self._get_events_sender().send_game_events([pick_item])

class GainMaterialEventHandler(object):

    def __init__(self, item_reader, game_location,
                  timer):
        self.__item_reader = item_reader
        self.__game_location = game_location
        self.__timer = timer

    def _get_timer(self):
        return self.__timer

    def get_game_loc(self):
        return self.__game_location

    def handle(self, event_to_handle):
        try:
            gameObject = self.__game_location.get_object_by_id(
                event_to_handle.objId
            )
            self.updateJobDone(gameObject)
            if event_to_handle.action == 'start':
                    ms1=event_to_handle.jobEndTime-((event_to_handle.jobEndTime/1000)*1000)
                    s1=(event_to_handle.jobEndTime/1000)-(((event_to_handle.jobEndTime/1000)/60)*60)
                    m1=((event_to_handle.jobEndTime/1000)/60)-((((event_to_handle.jobEndTime/1000)/60)/60)*60)
                    h1=((event_to_handle.jobEndTime/1000)/60)/60
                    ms2=self._get_timer()._get_current_client_time()-((self._get_timer()._get_current_client_time()/1000)*1000)
                    s2=(self._get_timer()._get_current_client_time()/1000)-(((self._get_timer()._get_current_client_time()/1000)/60)*60)
                    m2=((self._get_timer()._get_current_client_time()/1000)/60)-((((self._get_timer()._get_current_client_time()/1000)/60)/60)*60)
                    h2=((self._get_timer()._get_current_client_time()/1000)/60)/60
                    logger.info("Начата работа" + '. jobEndTime:'
                                + str(h1)+':'+str(m1)+':'+str(s1)+'.'+str(ms1) +
                                ', current time:' +
                                str(h2)+':'+str(m2)+':'+str(s2)+'.'+str(ms2))
                    gameObject.target = dict2obj({'id': event_to_handle.targetId})
                    gameObject.jobStartTime = event_to_handle.jobStartTime
                    gameObject.jobEndTime = event_to_handle.jobEndTime
            elif event_to_handle.action == 'stop':
                logger.info("Окончена работа")
        except:
            pass

    def updateJobDone(self, wood_grave):
        if hasattr(wood_grave, 'jobEndTime'):
            logger.info("Время окончания работы:")
            nextplay=int(wood_grave.jobEndTime)
            x1=int(wood_grave.jobEndTime)
            ms=nextplay-((nextplay/1000)*1000)
            s=(nextplay/1000)-(((nextplay/1000)/60)*60)
            m=((nextplay/1000)/60)-((((nextplay/1000)/60)/60)*60)
            h=((nextplay/1000)/60)/60
            logger.info(str(h)+':'+str(m)+':'+str(s)+'.'+str(ms))
            logger.info("Текущее время:")
            nextplay=int(self._get_timer()._get_current_client_time())
            ms1=nextplay-((nextplay/1000)*1000)
            s1=(nextplay/1000)-(((nextplay/1000)/60)*60)
            m1=((nextplay/1000)/60)-((((nextplay/1000)/60)/60)*60)
            h1=((nextplay/1000)/60)/60
            logger.info(str(h1)+':'+str(m1)+':'+str(s1)+'.'+str(ms1))
            logger.info("Время на работу:")
            nextplay1=(h*60*60*1000)+(m*60*1000)+(s*1000)+ms
            nextplay2=(h1*60*60*1000)+(m1*60*1000)+(s1*1000)+ms1
            nextplay=nextplay2-nextplay1
            ms=nextplay-((nextplay/1000)*1000)
            s=(nextplay/1000)-(((nextplay/1000)/60)*60)
            m=((nextplay/1000)/60)-((((nextplay/1000)/60)/60)*60)
            h=((nextplay/1000)/60)/60
            logger.info(str(h)+':'+str(m)+':'+str(s)+'.'+str(ms))
            if (self._get_timer().has_elapsed(wood_grave.jobEndTime)):
                if hasattr(wood_grave, 'target'):
                    target_id = wood_grave.target.id
                    target = self.get_game_loc().get_object_by_id(target_id)
                    target.materialCount -= 1
                    target_item = self.__item_reader.get(target.item)
                    logger.info("Материал добыт")
                    wood_grave.materials.append(target_item.material)
                    if target.materialCount == 0:
                        logger.info("Ресурсы исчерпаны!")
                        box_item = self.__item_reader.get(target_item.box)
                        new_obj = dict2obj({'item': '@' + box_item.id,
                                            'type': GamePickup.type,
                                            'id': target_id})
                        self.get_game_loc().remove_object_by_id(target_id)
                        self.get_game_loc().append_object(new_obj)
                        logger.info(u"'%s' превращён в '%s'" %
                                    (target_item.name, box_item.name))
                        # add free brains
                        delattr(wood_grave, 'target')
                delattr(wood_grave, 'jobEndTime')
        else:
            logger.info("Ещё не конец работы")


class TraderWork(ResourcePicker):
                
    def get_worker_types(self):
        return [GameTraderGrave.type, GameTraderGraveWithBrains.type]
    
    def perform_action(self):
        graves = self._get_game_location().get_all_objects_by_types(self.get_worker_types())
        for grave in graves:

            # Если торговец не работает
            if not grave.started:

                # Получаем его название
                grave_name = self._get_item_reader().get(grave.item).name
                
                # Выполняем запрос на сервер
                logger.info(u'Выгоняем работать %s %i' % (grave_name, grave.id))
                grave_start_event = {u'type': u'item', u'action': u'start', u'objId': grave.id}
                self._get_events_sender().send_game_events([grave_start_event])

                # Исправляем game_state, чтобы при следующем цикле он не посчитал торговца не рабочим
                grave.started = True
