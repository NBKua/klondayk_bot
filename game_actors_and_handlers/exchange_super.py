# coding=utf-8
import logging
from math import ceil
from game_state.game_types import GameBuilding
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict


logger = logging.getLogger(__name__)

class ExchangeCollections(BaseActor):
    def perform_action(self):
        
        # Сколько оставлять коллекций
        collections = {
                  #"C_1":10000,         # Звёздная
                  "C_2":10,         # Луксорская
                  #"C_3":10000,         # Байкерская
                  #"C_4":10000,         # Знаков
                  #"C_5":10000,         # Ручная
                  #"C_6":10000,         # Обувная
                  "C_7":10,         # Страшная
                  #"C_8":10000,         # Строительная
                  #"C_9":10000,         # Столовая
                  #"C_10":10000,        # Редкая
                  #"C_11":10000,        # Автомобильная
                  #"C_12":10000,        # Туристическая
                  #"C_13":10000,        # Домашняя
                  #"C_14":10000,        # Игрушек
                  #"C_15":10000,        # Ёлочная
                  #"C_16":10000,        # Кролика
                  #"C_17":10000,        # Цветов
                  #"C_18":10000,        # Деда Мороза
                  #"C_19":10000,        # Анти-зомби
                  #"C_20":10000,        # Брендов
                  #"C_21":10,        # Весенняя
                  "C_22":10,        # Тинейджерская
                  #"C_23":10000,        # Компа
                  "C_24":1,        # Морская
                  "C_25":1,        # Пляжная
                  "C_26":200,        # Майя
                  "C_27":1,        # Секретная
                  "C_28":1,        # Гипер
                  #"C_29":10000,        # Хэллоуин
                  #"C_30":10000,        # Президентская
                  #"C_31":10000,        # Зимняя
                  #"C_32":10000,        # Подземельная
                  "C_33":1,        # Любовная
                  #"C_34":10000,        # Адская
                  "C_35":1,        # Райская
                  #"C_36":10000,        # Японская
                  #"C_37":10000,        # Школьная
                  #"C_38":10000,        # Пиратская
                  #"C_39":10000,        # Рыбака
                  #"C_40":10000,        # Военная
                  #"C_41":10000,        # Футбольная
                  #"C_42":10000,        # Изумрудная
                  #"C_43":10000,        # Песочная 
                  #"C_44":10000,        # Котят
                  #"C_45":10000,        # Щенков
                  "C_46":1,        # Тропическая
                  "C_47":1,        # Плохая
                  #"C_48":10000,        # Палача
                  "C_49":1,        # Фобий
                  "C_50":1,        # Вкусная
                  "C_51":1         # Временная
                  }
                  
        # Словарь названий коллекций          
        name = {"C_1":u"Звёздная","C_2":u"Луксорская","C_3":u"Байкерская","C_4":u"Знаков","C_5":u"Ручная","C_6":u"Обувная","C_7":u"Страшная","C_8":u"Строительная","C_9":u"Столовая","C_10":u"Редкая","C_11":u"Автомобильная","C_12":u"Туристическая","C_13":u"Домашняя","C_14":u"Игрушек","C_15":u"Ёлочная","C_16":u"Кролика","C_17":u"Цветов","C_18":u"Деда Мороза","C_19":u"Анти-зомби","C_20":u"Брендов","C_21":u"Весенняя","C_22":u"Тинейджерская","C_23":u"Компа","C_24":u"Морская","C_25":u"Пляжная","C_26":u"Майя","C_27":u"Секретная","C_28":u"Гипер","C_29":u"Хэллоуин","C_30":u"Президентская","C_31":u"Зимняя","C_32":u"Подземельная","C_33":u"Любовная","C_34":u"Адская","C_35":u"Райская","C_36":u"Японская","C_37":u"Школьная","C_38":u"Пиратская","C_39":u"Рыбака","C_40":u"Военная","C_41":u"Футбольная","C_42":u"Изумрудная","C_43":u"Песочная","C_44":u"Котят","C_45":u"Щенков","C_46":u"Тропическая","C_47":u"Плохая","C_48":u"Палача","C_49":u"Фобий","C_50":u"Вкусная","C_51":u"Временная"}          
                  
                   
                  
        # Получаем количество на складе                             
        cl_items = obj2dict(self._get_game_state().get_state().collectionItems)
        for collection in collections: # Создаём item всех элементов         
            element_1 = collection + "_1"
            element_2 = collection + "_2"
            element_3 = collection + "_3"
            element_4 = collection + "_4"
            element_5 = collection + "_5"
            
            # Проверка на наличие собранной коллекции
            if (element_1 in cl_items) and (element_2 in cl_items) and (element_3 in cl_items) and (element_4 in cl_items) and (element_5 in cl_items):
                # И вычисляем сколько обменять
                count = min(cl_items[element_1],cl_items[element_2],cl_items[element_3],cl_items[element_4],cl_items[element_5]) - collections[collection]
                if count > 0:
                    event = [{"type":"item","count":count,"itemId":collection,"action":"collect"}]
                    self._get_events_sender().send_game_events(event)
                    logger.info(u"Обменяли %d коллекций '%s' "%(count,name[collection]))
                    self._get_game_state().remove_from_storage('@'+element_1, cl_items[element_1] - count)
                    self._get_game_state().remove_from_storage('@'+element_2, cl_items[element_2] - count)
                    self._get_game_state().remove_from_storage('@'+element_3, cl_items[element_3] - count)
                    self._get_game_state().remove_from_storage('@'+element_4, cl_items[element_4] - count)
                    self._get_game_state().remove_from_storage('@'+element_5, cl_items[element_5] - count)
                    cl_items[element_1] -= count
                    cl_items[element_2] -= count
                    cl_items[element_3] -= count
                    cl_items[element_4] -= count
                    cl_items[element_5] -= count
                    
        self._get_game_state().get_state().collectionItems=dict2obj(cl_items)