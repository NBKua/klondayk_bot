# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict
from game_state.game_types import GamePickPickup, GamePickItem, GamePickup
from game_actors_and_handlers.tree_plant import TreePlant

logger = logging.getLogger(__name__)

class PiratePut(BaseActor):
    
    def perform_action(self):
        num = 1              # партиями по ... шт.
        #------------------------------------------

        """
        # инфа
        for object in self._get_game_location().get_game_objects():
            print u'ищем...'
            if object.item[:4] == '@CH_':   
                print 'FIND: ', object.item, ' id = ', object.id
                print "Find ", str(obj2dict(object))         
                raw_input('-------------   END   ---------------')
        """
                
        """
        # Убираем ненужное
        for object in self._get_game_location().get_game_objects():
            print u'ищем...'
            if object.item[:16] == '@PIRATE_CAPTURE_':   
                print 'FIND: ', object.item, ' id = ', object.id
                print "Find ", str(obj2dict(pirate_obj)) 
                self._get_events_sender().send_game_events([{"type":"item","action":"moveToStorage","objId":object.id}])        
        raw_input('-------------   END   ---------------')
        """

        current_loc = self._get_game_state().get_location_id()
        storage = self._get_game_state().get_state().storageGameObjects
        next_id = max([_i.maxGameObjectId for _i in self._get_game_state().get_state().locationInfos] +[_m.id for _m in self._get_game_location().get_game_objects()]) + 1
        num_put = 0
        for pirate_obj in storage:                                 
            if num_put == num: break
            if not hasattr(pirate_obj, 'item'): continue
            if pirate_obj.item[:11] == '@PIRATE_BOX' and pirate_obj.item[:13] == '@SYMBOL_D_BOX':     #BIRTHDAY_GIFT_BOX4
                #print "Find ", str(obj2dict(pirate_obj))     
                obj = self._get_item_reader().get(pirate_obj.item)
                #print 'obj ', obj
                #logger.info(str(obj2dict(obj)).encode('utf-8'))
                space_crd = self.space(current_loc, obj)
                #print space_crd
                #raw_input('-------------   END   ---------------')  
                
                if space_crd == []: continue
                                
                if pirate_obj.count > num - num_put:
                    run = num - num_put
                else:
                    run = pirate_obj.count
                
                #events = []
                for n in range(run):                               
                    if n < len(space_crd):
                        k = space_crd[n]
                    else:
                        break

                    if len(k) == 5:
                        x = int(k[:3])
                        y = int(k[3:])
                    elif len(k) == 4:
                        if current_loc == u'main' and int(k[:2])<13:
                            x = int(k[:3])
                            y = int(k[3:])
                        else:                           
                            x = int(k[:2])
                            y = int(k[2:])
                    elif len(k) == 2:
                        x = int(k[:1])
                        y = int(k[1:])
                    else:
                        if k[0] == '8' or k[0] == '9':
                            x = int(k[:1])
                            y = int(k[1:])
                        else:
                            x = int(k[:2])
                            y = int(k[2:])
                  
                    event = {
                        "x":x,
                        "y":y,
                        "action":"placeFromStorage",
                        "itemId":pirate_obj.item[1:],
                        "type":"item",
                        "objId":next_id}
                    #print event 
                    self._get_events_sender().send_game_events([event])
                    #events.append(event)
                    #print u''+str(num_put)+u" Ставим "+pirate_obj.item+u" на X/Y: "+str(x)+u"/"+str(y)
                    logger.info(u''+str(num_put)+u" Ставим "+pirate_obj.item+u" на X/Y: "+str(x)+u"/"+str(y))
                    # добавляем инфу
                    self._get_game_state().get_state().gameObjects.append(dict2obj({u'item': pirate_obj.item, u'y': str(y), u'x': str(x), u'type': u'chop', u'id': next_id}))#, "chopCount":obj.chopCount}))
                    next_id += 1
                    num_put += 1                                       
                    
                #self._get_events_sender().send_game_events([events])                    
                # учёт
                if run == pirate_obj.count:
                    self._get_game_state().get_state().storageGameObjects.remove(pirate_obj)
                else:
                    pirate_obj.count -= run
        logger.info(u"Поставили "+str(num_put)+u" предметов")
        
        #raw_input('-------------   END   ---------------')
        #event = {"action":"placeFromStorage","x":41,"y":62,"itemId":"CH_STONE_05","type":"item","objId":18635}
        #event = {'itemId': u'CH_STONE_09', 'action': 'placeFromStorage', 'objId': 18636L, 'y': 48, 'x': 12, 'type': 'item'}
        # на складе {u'count': 16L, u'item': u'@CH_STONE_09'}                    
        # obj = {u'buyCoins': 0L, u'gift': False, u'level': 1L, u'chopCount': 18L, u'moved': True, u'chopInstrumentType': u'@CIT_HAMMER', u'type': u'chop', u'id': u'CH_STONE_09'}
        # стоИт {u'rotate': 0L, u'chopCount': 18L, u'item': u'@CH_STONE_09', u'y': 51L, u'x': 19L, u'type': u'chop', u'id': 18626L}        
        
        
    def space(self, location, need, submap=[]):
        for rect in list(need.rects):
            if rect.rectW > 0 and rect.rectH > 0:
                need.w = int(rect.rectW)
                need.h = int(rect.rectH)

        #file = open('space.txt', 'a')                
        """
        logger.info(u'Объект need:')
        logger.info(str(obj2dict(need)).encode('utf-8'))
        logger.info('  ')
        file.write(u'Объект need: \n'.encode('utf-8'))
        file.write(str(obj2dict(need))+'\n'.encode('utf-8'))
        file.write(u' \n')
        """
                
        crd, bad_crd = self.get_coords(location, submap)
        obj_cache = {}
        space_crd = []
            
        """
        logger.info(u'Объект crd:')
        logger.info(str(obj2dict(crd)).encode('utf-8'))
        logger.info('  ')
        file.write(u'Объект crd: \n'.encode('utf-8'))
        file.write(str(obj2dict(crd))+'\n'.encode('utf-8'))
        file.write(u' \n')
        file.write(u'Начальные bad_crd: \n'.encode('utf-8'))
        file.write(str(obj2dict(bad_crd))+'\n'.encode('utf-8'))
        file.write(u' \n')        
        """

        #перебор объектов на острове
        objects = self._get_game_location().get_game_objects()
        for object in list(objects):
            if not hasattr(object, 'x') or not hasattr(object, 'item'):
                continue
            x = object.x
            y = object.y

            if not object.item in obj_cache:
                object_item = self._get_item_reader().get(object.item)
                obj_cache[object.item] = object_item
            else:
                object_item = obj_cache[object.item]
                
            #sms = u'Занято '+object_item.name+str(x)+' '+str(y)+u' размеры: '+str(object_item.rects)+'\n'
            #file.write(sms.encode('utf-8'))

            for rect in list(object_item.rects):
                
                h = rect.rectH
                if rect.rectX < 0:
                    x = int(x) + rect.rectX
                    w = rect.rectW + (rect.rectX*-1)
                else:
                    w = rect.rectW + rect.rectX
                if rect.rectY < 0:
                    y = int(y) + rect.rectY
                    h = rect.rectH + (rect.rectY*-1)
                else:
                    h = rect.rectH + rect.rectY
                                     
                for ix in range(w):
                    for iy in range(h):
                        k = str(int(x) + ix)+''+str(int(y) + iy)
                        if not k in bad_crd:
                            bad_crd.append(k)
                            """
                            logger.info(u'Добавляем занятые координаты '+str(x)+' '+str(ix)+' '+str(y)+' '+str(iy)+' : '+k)
                            sms = u'Добавляем занятые координаты '+str(x)+' '+str(ix)+' '+str(y)+' '+str(iy)+' : '+k+'\n'
                            file.write(sms.encode('utf-8'))
                            """
        """                    
        #logger.info(str(obj2dict(bad_crd)).encode('utf-8'))
        file.write(u'Полные bad_crd: \n'.encode('utf-8'))
        file.write(str(obj2dict(bad_crd))+'\n'.encode('utf-8'))
        file.write(u' \n')
        """

        W = crd['x2'] - crd['x1'] - need.w + 2
        H = crd['y2'] - crd['y1'] - need.h + 2

        for iw in range(W):
            iw += crd['x1']
            for ih in range(H):
                ih += crd['y1']
                if (str(iw)+''+str(ih)) in bad_crd: #занято
                    continue
                good = 1
                add = []
                for ix in range(need.w):
                    for iy in range(need.h):
                        k = str(iw+ix)+''+str(ih+iy)
                        if k in bad_crd: #занято
                            good = 0
                            break
                        else:
                            add.append(k)
                    if good == 0:
                        break
                if good == 1:
                    #logger.info(u'Свободные '+need.id+u' на X: '+str(iw)+u', Y: '+str(ih))
                    space_crd.append(str(iw)+''+str(ih))
                    bad_crd.extend(add)

        """
        logger.info('Свободные координаты установки:')
        logger.info(str(obj2dict(space_crd))+'\n'.encode('utf-8'))
        logger.info('  ')
        file.write(u'Свободные координаты установки: \n'.encode('utf-8'))
        file.write(str(obj2dict(space_crd))+'\n'.encode('utf-8'))
        file.write(u' \n')
        """
        return space_crd
        
                       
    def get_coords(self, ostrov, submap=[]):                
         
        # Map world   Домашний
        if(ostrov in ['main']): 
            map = [ str(i)+''+str(j) for i in range(48,62) for j in range(12,48)]
            add = [ str(i)+''+str(j) for i in range(54,60) for j in range(48,100)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(62,112) for j in range(30,48)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(14,62) for j in range(0,12)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(112,128) for j in range(30,112)]
            map.extend(add)
            if submap != []:        
                if not u'снизу от дороги' in submap:
                    add = [ str(i)+''+str(j) for i in range(14,54) for j in range(48,100)]
                    map.extend(add)           
                if not u'сверху от дороги' in submap:
                    add = [ str(i)+''+str(j) for i in range(60,112) for j in range(48,100)]
                    map.extend(add)  
                if not u'за забором' in submap:
                    add = [ str(i)+''+str(j) for i in range(14,48) for j in range(12,48)]
                    map.extend(add) 
                if not u'на горе' in submap:
                    add = [ str(i)+''+str(j) for i in range(62,128) for j in range(0,30)]
                    map.extend(add)                        
            return {'x1':14, 'x2':127, 'y1':0, 'y2':99}, map                              
                    
        # Map isle_01   Веры, Мечты
        if(ostrov in ['isle_dream', 'isle_faith']):
            map = [ str(i)+''+str(j) for i in range(14,16) for j in range(14,16)]
            add = [ str(i)+''+str(j) for i in range(12,14) for j in range(14,64)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(12,18) for j in range(74,76)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(40,82) for j in range(74,76)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(82,84) for j in range(72,76)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(82,84) for j in range(14,22)]
            map.extend(add)                                     
            return {'x1':12, 'x2':83, 'y1':14, 'y2':75}, map                      

        # Map isle_02   Альфа, Омега, Пик Админа, Ужасный, Чудовища, Майя, звёздный, гигантов 
        if(ostrov in ['isle_alpha', 'isle_omega', 'isle_scarecrow', 'isle_elephant', 'isle_monster', 'isle_02', 'isle_star', 'isle_giant']):
            map = [ str(i)+''+str(j) for i in range(10,12) for j in range(10,12)]
            add = [ str(i)+''+str(j) for i in range(10,12) for j in range(42,44)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,44) for j in range(42,44)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,44) for j in range(10,12)]
            map.extend(add)
            return {'x1':10, 'x2':43, 'y1':10, 'y2':43}, map                         
                        
        # Map isle_03   Любви, X, Песочный, Необитаемый 
        if(ostrov in ['isle_03', 'isle_x', 'isle_sand', 'isle_desert']):
            map = []
            return {'x1':16, 'x2':65, 'y1':14, 'y2':71}, map                                 
        
        # Map isle_04   Надежды, Страшный
        if(ostrov in ['isle_hope', 'isle_scary']):
            map = [ str(i)+''+str(j) for i in range(12,14) for j in range(12,14)]
            add = [ str(i)+''+str(j) for i in range(46,50) for j in range(12,14)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(48,50) for j in range(34,42)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(48,50) for j in range(72,74)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(12,20) for j in range(72,74)]
            map.extend(add)   
            return {'x1':12, 'x2':49, 'y1':12, 'y2':73}, map 
             
        # Map isle_05   Город-призрак, Секретный 
        if(ostrov in ['isle_emerald', 'isle_01']):
            map = [ str(i)+''+str(j) for i in range(16,20) for j in range(12,16)]
            add = [ str(i)+''+str(j) for i in range(70,72) for j in range(30,38)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(70,72) for j in range(70,72)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(16,18) for j in range(64,72)]
            map.extend(add)   
            return {'x1':16, 'x2':71, 'y1':12, 'y2':71}, map                         

        # Map isle_snow1   Дремучий, Мобильный, Маленькой ёлочки, Огромной ёлки
        if(ostrov in ['isle_wild', 'isle_mobile', 'isle_small', 'isle_xxl']):
            map = [ str(i)+''+str(j) for i in range(8,12) for j in range(6,8)]
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(8,10)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,46) for j in range(6,8)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,46) for j in range(8,10)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(44,46) for j in range(42,46)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(42,44) for j in range(44,46)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(44,46)]
            map.extend(add)   
            return {'x1':8, 'x2':45, 'y1':6, 'y2':45}, map 
               
        # Map isle_snow2   Полярной ночи, НЛО, Лысая гора, Большой ёлки, Лунный, Вишнёвый
        if(ostrov in ['isle_polar', 'isle_ufo', 'isle_halloween', 'isle_large', 'isle_moon', 'isle_light']):
            map = [ str(i)+''+str(j) for i in range(8,12) for j in range(6,10)]
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(44,46)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,46) for j in range(44,46)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,46) for j in range(42,44)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,46) for j in range(6,8)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,46) for j in range(8,10)]
            map.extend(add)             
            return {'x1':8, 'x2':45, 'y1':6, 'y2':45}, map   
 