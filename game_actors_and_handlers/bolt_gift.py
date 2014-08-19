# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_types import GameSendGift

logger = logging.getLogger(__name__)

class BoltGift(BaseActor):

    def perform_action(self):
      nut_count = 1   # Сколько необходимо гаек
      bolt_count = 0  # Количество необходимых гаек болтов
      send_user = '18318155742226352457'#'6745101591662640459' # ID игрока, кому шлем
      event = []
      for _i in range(nut_count):
        send_gift={"item":"@CR_53",
                   "msg":"",
                   "count":1,
                   "user":send_user}
        event.append(GameSendGift(gift=send_gift))
      send_gift={"item":"@BELL",
                   "msg":u"привет)))",
                   "count":bolt_count,
                   "user":send_user}
      event.append(GameSendGift(gift=send_gift))
      self._get_events_sender().send_game_events(event) 
      logger.info( u'Отослал ' +(str( bolt_count) +u' ,болтов и '+(str( nut_count) +u'гаек.')))
