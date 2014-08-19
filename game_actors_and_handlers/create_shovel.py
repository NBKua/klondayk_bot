# coding=utf-8
# Создание лопат в Глаз-алмаз
import logging
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameStone, GameGainItem, GamePickup, GameBuilding
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class CreateShovelExtra(BaseActor):

    # Находим нужное здание по его идентификатору
    def get_building_by_Id(self, obj_Id):
        buildings = self._get_game_location().get_all_objects_by_type(
                        GameBuilding.type)
        for building in buildings:
            if obj_Id in building.item and building.level == 3:
                return building
        return None

    # Находим на складе необходимые материалы, проверяем соответсвие необходимому количеству и получаем коэфициент, сколько раз создавать
    def lacking_in_storage(self, _one, _one_count, _two, _two_count, _money, _count):

        ratio_one = 0
        ratio_two = 0
        storage_one = self._get_game_state().count_in_storage(_one) - _count
        if _two == "@COINS":
            storage_two = self._get_game_state().get_state().gameMoney - _money
        else:
            storage_two = self._get_game_state().count_in_storage(_two) - _count
        if storage_one >= _one_count: ratio_one = storage_one / _one_count
        if storage_two >= _two_count: ratio_two = storage_two / _two_count
        index = min(ratio_one,ratio_two)
        print index, max(ratio_one,ratio_two)
        return index


    def perform_action(self):

        money_min = 30000000 # Сколько оставлять монет
        craft_id = 2 # 1-за деньги и бамбук, 2 - за доски и гвозди
        min_count = 50 # Сколько оставлять гвоздей или досок (берем по минимальному из двух), если craft_id = 2; либо бамбука, если craft_id = 1
        location_id = "isle_02" # Локация, на которой стоит Глаз-алмаз
        Build_Id = "B_EYE" # Глаз-алмаз
        crafts = self._get_item_reader().get("@B_EYE").crafts # Получаем данные о крафтинге здания

        event = [] # Переменная для списка эвентов

        current_loc = self._get_game_state().get_location_id() # Получаем текущую локацию

        if craft_id == 1 and (self._get_game_state().get_state().gameMoney <= money_min):
            return

        if current_loc == location_id:
            build = self.get_building_by_Id(Build_Id)
            if build:
                for craft in crafts:
                    if int(craft.id) == craft_id:
                        stuff_one = craft.materials[0].item
                        stuff_one_name = self._get_item_reader().get(stuff_one).name
                        stuff_one_count = craft.materials[0].count
                        stuff_two = craft.materials[1].item
                        stuff_two_name = self._get_item_reader().get(stuff_two).name
                        stuff_two_count = craft.materials[1].count
                        result_count = craft.resultCount
                        result = craft.result

                logger.info(u'На складе %d лопат.' % self._get_game_state().count_in_storage(result))

                ratio = self.lacking_in_storage(stuff_one, stuff_one_count, stuff_two, stuff_two_count, money_min, min_count)

                for _i in range(ratio):
                    event.append({"itemId":craft_id,"objId":build.id,"action":"craft","type":"item"})
                self._get_events_sender().send_game_events(event)
                self._get_game_state().remove_from_storage(stuff_one, stuff_one_count*ratio)
                if stuff_two == "@COINS":
                    self._get_game_state().get_state().gameMoney -=stuff_two_count*ratio
                else:
                    self._get_game_state().remove_from_storage(stuff_two,stuff_two_count*ratio)
                self._get_game_state().add_from_storage(result,result_count*ratio)

                logger.info(u'Создано %d лопат(а)'% (ratio*result_count))
                logger.info(u'На складе %d лопат.' % self._get_game_state().count_in_storage(result))
