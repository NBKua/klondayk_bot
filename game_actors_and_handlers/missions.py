# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict

logger = logging.getLogger(__name__)

class GetMissionsBot(BaseActor):

    def perform_action(self):
        get_event={
            "type":"action",
            "id":123123,
            "action":"getMissions"
            }
        self._get_events_sender().send_game_events([get_event])


class ViewMissions(object):
    def __init__(self, itemReader, setting_view):
        self.__item_reader = itemReader
        self.__setting_view = setting_view

    def handle(self, event_to_handle):
        if event_to_handle is None:
            logger.critical("OMG! No such object")
            return
        else:
            missions=obj2dict(event_to_handle)
            logger.info(u'Трофеи:')
            if missions["action"]=="getMissions":
                for id in missions["missions"]:
                    if id["type"]=="achievement":
                        item=obj2dict(self.__item_reader.get(id["item"]))
                        if (id['completed']+1)==4: 
                            if len(item["name"])>13: logger.info(u'\t%s:\tзавершен, получен приз "%s"'%(item["name"],self.__item_reader.get(item['achievementPrizes'][2]["prizes"][0]["item"]).name))
                            else: logger.info(u'\t%s:\t\tзавершен, получен приз "%s"'%(item["name"],self.__item_reader.get(item['achievementPrizes'][2]["prizes"][0]["item"]).name))
                        else: 
                            try: num1=id['tasks'][item['id']+'_'+str(id['completed']+1)]["count"]
                            except: num1=id['tasks'][item['id']+'-'+str(id['completed']+1)]["count"]
                            try:
                                for i in item['tasks']: 
                                    if (item['id']+'_'+str(id['completed']+1))==i['id']:
                                        num2=i["count"]
                            except:
                                for i in item['tasks']: 
                                    if (item['id']+'-'+str(id['completed']+1))==i['id']:
                                        num2=i["count"]
                            if len(item["name"])>13: logger.info(u'\t%s:\tстадия %d (%d/%d)'%(item["name"],id['completed']+1,num1,num2))
                            else: logger.info(u'\t%s:\t\tстадия %d (%d/%d)'%(item["name"],id['completed']+1,num1,num2))
                        #raw_input()
            logger.info(u'')