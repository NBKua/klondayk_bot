# coding=utf-8
import sys
import logging
import  random  as  random_number
from game_state.game_types import GameWoodGrave, GameWoodGraveDouble,\
    GamePickItem, GameWoodTree, GameGainItem, GamePickup, GameDigItem
from game_state.game_event import dict2obj, obj2dict
from game_actors_and_handlers.base import BaseActor

logger = logging.getLogger(__name__)


class FriendDigger(BaseActor):
    def perform_action(self):
          #logger.info(u"######### Идем к другу ###########")
          #go_to_friend = {"action":"gameState","locationId":"main","user":'201018303',"objId":None,"type":"gameState"}#{"id":8,"action":"gameState","objId":null,"locationId":"main","user":"144371056","type":"gameState"} #,"id":46667
          #friends = ['8477452','22656865','27505179','107183826','68030140','163206097']#'476111',
          friends = self._get_options()
          #            Юдо              Чудо
          #friends = ['7942552'] + friends
          #friends = ['35908611','7942552'] + friends
          objtypes = ['decoration']
          myid = '35834355'
          self._get_game_state().shovel = 0
          if not hasattr(self._get_game_state(),'countfnyt'):self._get_game_state().countfnyt = 0
          if not hasattr(self._get_game_state(), 'countnyt'):self._get_game_state().countnyt = 0
          if not hasattr(self._get_game_state(), 'sendNewYearGift'):self._get_game_state().sendNewYearGift = 0
          if not hasattr(self._get_game_state(), 'gameObjects') and self._get_game_state().countfnyt < len(friends):
            user = friends[self._get_game_state().countfnyt]
            print (u"######### Идем к другу "+str(user)+" "+str(self._get_game_state().countfnyt+1)+"/"+str(len(friends))+" #########").encode('cp866')
            self._get_events_sender().send_game_events([{"action":"gameState","locationId":"main","user":str(user),"objId":None,"type":"gameState"},{"type":"players","action":"getInfo","players":[str(user)]}])
            self._get_game_state().countfnyt += 1
          elif hasattr(self._get_game_state(), 'gameObjects'):# and 
            open('objects.txt', 'a').write(str(friends[self._get_game_state().countfnyt])+"\n")
            print "############### gameObjects #################"
            countnyt = 0
            countmyg = 0
            countpickup = 0
            objssvl = []
            if hasattr(self._get_game_state(),'alldigged'):alldigged = 1
            else: alldigged = 0
            for object in self._get_game_state().gameObjects:
                if self._get_game_state().countnyt + countnyt < 148:
                    if hasattr(object, 'type'):
                        tf = 0
                        if object.type == 'newYearTree':
                            tf = 1
                            usrs = len(object.users)
                            #object.users = usrs
                            #open('newyeartree.txt', 'a').write(str(obj2dict(object))+"\n")
                        if tf == 1 and not hasattr(self._get_game_state(), 'nytend'): 
                            print (u"Ёлка !!!").encode('cp866')
                            #open('gameObjects.txt', 'a').write(str(obj2dict(object))+"\n")
                            #open('newyeartree.txt', 'a').write(object.item + " UsersGift:" + str(len(object.users)) + "\n")
                            tf = 1
                            f = 0
                            #Ёлки разной ёмкости. указано не точно.
                            if object.item == u'@B_SPRUCE_SMOLL' and len(object.users) < 3: f = 1
                            if object.item == u'@B_SPRUCE_MIDDLE' and len(object.users) < 6: f = 1
                            if object.item == u'@B_SPRUCE_BIG' and len(object.users) < 15: f = 1
                            #if object.item == u'@B_BASKETS_EASTER_1' and len(object.users) < 15: f = 1
                            #if object.item == u'@B_BASKETS_EASTER_2' and len(object.users) < 7: f = 1
                            #if object.item == u'@B_BASKETS_EASTER_3' and len(object.users) < 3: f = 1
                            for user in object.users:
                                if user.id == myid:
                                    countmyg+=1#print "MyGift"
                                    f = 0
                                    break
                                
                            #if not check_no_my_gift(object.users): f = 1
                            if self._get_game_state().countnyt + countnyt > 151 or hasattr(self._get_game_state(),'nyna'):
                                self._get_game_state().nytend = 1
                                print "################## END ####################"
                            f = 0 #0 - Пряники не ложим, 1 - пряники ложим
                            if f == 1:
                                # Ложим пряник
                                #open('newyeartree.txt', 'a').write(str(obj2dict(object)) + "\n")
                                self._get_events_sender().send_game_events([{"itemId":"CAKE_PACK_FREE1","action":"remoteNewYear","type":"item","objId":object.id}])
                                countnyt+=1
                                pass
                            else: print "NO"
                        # Вскрываем сундук
                        if tf == 0 and object.type == 'pickup':
                            open('sunduki.txt', 'a').write(str(obj2dict(object)) + "\n")
                            self._get_events_sender().send_game_events([{"action":"pick","type":"item","objId":object.id}])
                            countpickup+=1
                            tf = 2
                        # Добавляем в список объекты для копания клада
                        if tf == 0 and alldigged == 0:
                            for objtype in objtypes:
                                if object.type == objtype:
                                    if object.item == '@DS_SYMBOL_E' or object.item == '@D_BALLOONS' or object.item == '@D_SAKURASMALL':
                                        print object.item,object.id
                                        objssvl.append(object)
                                        break                            
                        if tf == 0:
                            open('objects.txt', 'a').write(str(obj2dict(object))+"\n")
            if hasattr(self._get_game_state(),'playersInfo'):
                open('objects.txt', 'a').write('-------------------------------------' + "\n")
                #open('objects.txt', 'a').write(str(obj2dict(self._get_game_state().playersInfo))+"\n")
                open('users.txt', 'a').write(str(obj2dict(self._get_game_state().playersInfo))+"\n")
                
            open('objects.txt', 'a').write('-------------------------------------' + "\n")
            countlop = 0
            if len(objssvl) > 0:
                for i in range(300):
                    objdig = random_number.choice(objssvl)
                    self._get_events_sender().send_game_events([{"objId":objdig.id,"x":objdig.x,"action":"remoteDig","y":objdig.y,"type":"item"}])
                    countlop+=1
                print (u"Использовал: "+str(countlop)+u" лопат").encode('cp866')
            elif alldigged == 1: print (u'Всё уже выкопано!').encode('cp866')
            else: print (u'Нечего копать!').encode('cp866')
            print (u"Вскрыли сундуков: "+str(countpickup)).encode('cp866')
            if hasattr(self._get_game_state(),'alldigged'): del self._get_game_state().alldigged
            del self._get_game_state().gameObjects
            self._get_game_state().countnyt += countnyt
            print (u"поЛожил пряник(ов): "+str(self._get_game_state().sendNewYearGift)+":"+str(self._get_game_state().countnyt)+"/"+str(countnyt)+" dub: "+str(countmyg)).encode('cp866')
            self._get_game_state().shovel = 0
            #if self._get_game_state().countfnyt + 1 > len(friends):sys.exit(0) 