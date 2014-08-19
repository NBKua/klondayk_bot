# coding=utf-8
################################   модуль написан DreamerAG  #######################
import logging
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameWoodTree, GameStone
import sys
##############################
from ctypes import windll
import sys

stdout_handle = windll.kernel32.GetStdHandle(-11)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
##############################
#import sys.stdout
logger = logging.getLogger(__name__)

class DigBot(BaseActor):
#class DigBot(object):
  def perform_action(self):
    friends=['3964456987234298509','14918235694863302451','7993204982920828146','4636772978653302992']#id друзей для закопки
    #friends = self._get_options()
    #обходим слоты для закопки и создаем список свободных слотов
    i=0
    freeslots=[]
    for burySlot in self._get_game_state().get_state().burySlots:
        if not hasattr(burySlot, 'user'):
            #print str(i) + " " + 'Free'
            freeslots.append(i)
        i+=1
    if freeslots == []: return #если все слоты заняты выходим из функции
    #распределяем друзей по слотам
    friendsslot=[]
    for slot in freeslots:
        #print u'Слот свободен: ' + str(slot+1)
        friendsslot.append(friends[slot])
    #запрашиваем инфу о друзьях
    if not hasattr(self._get_game_state(), 'playersInfo'):
        self._get_events_sender().send_game_events([{"type":"players","action":"getInfo","players":friendsslot}])
        logger.info(u"Получаем инфу о друге")
    elif hasattr(self._get_game_state(), 'digOut'):#обратный счетчик раскопки
        self._get_game_state().digOut -= 1
        #print self._get_game_state().digOut
        if self._get_game_state().digOut < 0: del self._get_game_state().digOut
    else:
        playersInfo = self._get_game_state().playersInfo
        #если закопаны, раскапываемся
        if 0:#freeslots != [] and hasattr(self._get_game_state().get_state(), 'buriedBy'):
            SetConsoleTextAttribute(stdout_handle, 0x0005 | 0x0008)
            logger.info(u'!!!! Раскапываемся !!!!').encode('cp866')
            SetConsoleTextAttribute(stdout_handle, 0x0002 | 0x0008)
            sys.stdout.flush()
            self._get_events_sender().send_game_events([{"user":"39245930","slot":-1,"type":"bury","action":"digOut"}])
            self._get_game_state().digOut = 90 #при interval = 4 т е устанавливаем счетчик раскопки
            return
        i=0
        for slot in freeslots:
            logger.info(str(len(playersInfo)))
            if i < len(playersInfo) and hasattr(playersInfo[i], 'buried'):
                SetConsoleTextAttribute(stdout_handle, 0x0005 | 0x0008)
                logger.info( u'Раскапываем: '),
                SetConsoleTextAttribute(stdout_handle, 0x0006 | 0x0008)
                sys.stdout.flush()
                logger.info(str(playersInfo[i].id))
                SetConsoleTextAttribute(stdout_handle, 0x0002 | 0x0008)
                sys.stdout.flush()
                cook_event = {"user":str(playersInfo[i].id),"type":"bury","action":"digOut"}
                self._get_events_sender().send_game_events([cook_event])
            elif i < len(playersInfo):
                SetConsoleTextAttribute(stdout_handle, 0x0004 | 0x0008)
                logger.info(u'Закапываем: '),
                SetConsoleTextAttribute(stdout_handle, 0x0006 | 0x0008)
                sys.stdout.flush()
                logger.info(str(playersInfo[i].id)),
                SetConsoleTextAttribute(stdout_handle, 0x0005 | 0x0008)
                sys.stdout.flush()
                logger.info(u' в слот '),
                SetConsoleTextAttribute(stdout_handle, 0x0007 | 0x0008)
                sys.stdout.flush()
                logger.info(str(slot+1))
                SetConsoleTextAttribute(stdout_handle, 0x0002 | 0x0008)
                sys.stdout.flush()
                cook_event = {"action":"bury","type":"bury","user":str(playersInfo[i].id),"slot":slot}
                self._get_events_sender().send_game_events([cook_event])
            i+=1
        del self._get_game_state().playersInfo
        self._get_game_state().digOut = 160
