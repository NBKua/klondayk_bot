# coding=utf-8
import logging
from game_actors_and_handlers.base import BaseActor
from game_state.game_event import dict2obj, obj2dict
import copy

logger = logging.getLogger(__name__)

class TreePlant(BaseActor):

    def perform_action(self):
        min_money = 0  # оставляем денег    
        # Что где сажаем   u'FT_CHERRY', u'FT_APPLE' , u'FT_MANDARINE', "FT_EYE"
        plant_tree = {
                #u'main':u'FT_CHERRY',               # Домашний
                #u'isle_polar':u'GROUND',                # Домашний
                #u'main':u'CANDY_BOX2',                # Домашний
                #u'isle_03':u'GROUND',             # Любви
                #u'isle_02':u'FT_CHERRY',             # Майя
                #u'isle_x':u'GROUND',              # X
                #u'isle_faith':u'FT_EYE',          # Веры
                #u'isle_hope':u'GROUND',           # Надежды
                #u'isle_scary':u'GROUND',          # Страшный
                #u'isle_alpha':u'GROUND',          # Альфа
                u'isle_omega':u'GROUND',          # Омега
                #u'isle_sand':u'FT_CHERRY',           # Песочный
                #u'isle_polar':u'FT_CHERRY',          # Полярной ночи
                #u'isle_wild':u'GROUND',           # Дремучий
                #u'isle_mobile':u'FT_CHERRY',         # Мобильный
                #u'isle_ufo':u'FT_CHERRY',            # НЛО
                #u'isle_dream':u'GROUND',          # Мечты
                #u'isle_scarecrow':u'FT_CHERRY',      # Пик Админа
                #u'isle_elephant':u'FT_CHERRY',       # Ужасный
                #u'isle_emerald':u'GROUND',        # Город Призрак
                #u'isle_monster':u'FT_CHERRY',        # Чудовища
                #u'isle_halloween':u'FT_CHERRY',      # Лысая гора
                #
                ###############     Платные     ###############
                #
                #u'isle_01':u'FT_CHERRY',             # Секретный
                #u'isle_small':u'FT_CHERRY',          # Маленькой ёлочки
                #u'isle_star':u'FT_CHERRY',           # Звездный
                #u'isle_large':u'FT_CHERRY',          # Большой ёлки
                #u'isle_moon':u'FT_CHERRY',           # Лунный
                #u'isle_giant':u'FT_CHERRY',          # Гигантов
                #u'isle_xxl':u'FT_CHERRY',            # Огромной ёлки
                #u'isle_desert':u'FT_CHERRY'          # Необитаемый
                }

        current_loc = self._get_game_state().get_location_id()
        if not current_loc in plant_tree:
            logger.info(u"Пропускаем "+current_loc)
            return 1
        need = plant_tree [current_loc]
                 
        next_id = max([_i.maxGameObjectId for _i in self._get_game_state().get_state().locationInfos]) + 1
        
        need = self._get_item_reader().get(need)
        space_crd = self.space(current_loc, need)
        build_cost = self._get_item_reader().get(need.id).buyCoins
        
        num = 0
        if space_crd:
            for k in space_crd:
                if len(k) == 5:
                    x = int(k[:3])
                    y = int(k[3:])
                elif len(k) == 4:
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
                    
                if self._get_game_state().get_state().gameMoney > min_money:
                    num += 1                
                    buy = {"x":x,"y":y,"action":"buy","itemId":need.id,"type":"item","objId":next_id}                    
                    self._get_events_sender().send_game_events([buy])
                    self._get_game_state().get_state().gameMoney -= build_cost
                    logger.info(u''+str(num)+u" Сажаем "+need.id+u" на X: "+str(x)+u", Y: "+str(y))
                    self._get_game_state().get_state().gameObjects.append(dict2obj({u'rotate': u'0L', u'fruitingCount': u'25L', u'fertilized': False, u'item': u'@'+need.id, u'jobFinishTime': u'79200000', u'jobStartTime': u'0', u'y': str(y), u'x': str(x), u'type': u'fruitTree', u'id': next_id}))
                    next_id += 1                     
                    


    def space(self, location, need):
        file = open('space.txt', 'a')
        for rect in list(need.rects):
            if rect.rectW > 0 and rect.rectH > 0:
                need.w = int(rect.rectW)
                need.h = int(rect.rectH)
                
        """
        logger.info(u'Объект need:')
        logger.info(str(obj2dict(need)).encode('utf-8'))
        logger.info('  ')
        file.write(u'Объект need: \n'.encode('utf-8'))
        file.write(str(obj2dict(need))+'\n'.encode('utf-8'))
        file.write(u' \n')
        """
                
        crd, bad_crd = self.get_coords(location)
        obj_cache = {}
        space_crd = []
        if bad_crd == []:
            return space_crd
            
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
                
            sms = u'Занято '+object_item.name+str(x)+' '+str(y)+u' размеры: '+str(object_item.rects)+'\n'
            file.write(sms.encode('utf-8'))

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

        W = crd['x2'] - crd['x1'] - need.w
        H = crd['y2'] - crd['y1'] - need.h

        for iw in range(W):
            iw += crd['x1']
            for ih in range(H):
                ih += crd['y1']
                if (str(iw)+''+str(ih)) in bad_crd: #занято
                    continue
                good = 1
                add = []
                for ix in range(need.w):
                    #ix += 1
                    for iy in range(need.h):
                        #iy += 1
                        k = str(iw+ix)+''+str(ih+iy)
                        if k in bad_crd:#занято
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
        
                       
    def get_coords(self, ostrov):
        # Map isle_01   Веры, Мечты
        if(ostrov in ['isle_dream', 'isle_faith']):
            map = [ str(i)+''+str(j) for i in range(14,16) for j in range(14,16)]
            add = [ str(i)+''+str(j) for i in range(12,14) for j in range(14,64)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(12,18) for j in range(74,78)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(40,82) for j in range(74,78)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(82,86) for j in range(72,78)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(82,86) for j in range(14,22)]
            map.extend(add)                                     
            return {'x1':12, 'x2':85, 'y1':14, 'y2':77}, map
         
        # Map world   Домашний
        if(ostrov in ['main']):
            map = [ str(i)+''+str(j) for i in range(48,62) for j in range(12,48)]
            add = [ str(i)+''+str(j) for i in range(54,60) for j in range(48,102)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(62,114) for j in range(30,48)]
            map.extend(add)
            return {'x1':14, 'x2':113, 'y1':12, 'y2':101}, map                        

        # Map isle_02   Альфа, Омега, Пик Админа, Ужасный, Чудовища, Майя, звёздный, гигантов 
        if(ostrov in ['isle_alpha', 'isle_omega', 'isle_scarecrow', 'isle_elephant', 'isle_monster', 'isle_02', 'isle_star', 'isle_giant']):
            map = [ str(i)+''+str(j) for i in range(10,12) for j in range(10,12)]
            add = [ str(i)+''+str(j) for i in range(10,12) for j in range(42,46)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,46) for j in range(42,46)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,46) for j in range(10,12)]
            map.extend(add)            
            return {'x1':10, 'x2':45, 'y1':10, 'y2':45}, map                         
                        
        # Map isle_03   Любви, X, Песочный, Необитаемый 
        if(ostrov in ['isle_03', 'isle_x', 'isle_sand', 'isle_desert']):
            map = [ str(i)+''+str(j) for i in range(10,12) for j in range(10,12)]
            add = [ str(i)+''+str(j) for i in range(10,12) for j in range(72,74)]
            map.extend(add)
            return {'x1':16, 'x2':67, 'y1':14, 'y2':73}, map                                 
        
        # Map isle_04   Надежды, Страшный
        if(ostrov in ['isle_hope', 'isle_scary']):
            map = [ str(i)+''+str(j) for i in range(12,14) for j in range(12,14)]
            add = [ str(i)+''+str(j) for i in range(46,52) for j in range(12,14)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(48,52) for j in range(34,42)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(48,52) for j in range(72,76)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(12,20) for j in range(72,76)]
            map.extend(add)   
            return {'x1':12, 'x2':51, 'y1':12, 'y2':75}, map 
             
        # Map isle_05   Город-призрак, Секретный 
        if(ostrov in ['isle_emerald', 'isle_01']):
            map = [ str(i)+''+str(j) for i in range(16,20) for j in range(12,16)]
            add = [ str(i)+''+str(j) for i in range(70,74) for j in range(30,38)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(70,74) for j in range(70,74)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(16,18) for j in range(64,74)]
            map.extend(add)   
            return {'x1':16, 'x2':73, 'y1':12, 'y2':73}, map                          

        # Map isle_snow1   Дремучий, Мобильный, Маленькой ёлочки, Огромной ёлки
        if(ostrov in ['isle_wild', 'isle_mobile', 'isle_small', 'isle_xxl']):
            map = [ str(i)+''+str(j) for i in range(8,12) for j in range(6,8)]
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(8,10)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,48) for j in range(6,8)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,48) for j in range(8,10)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(44,48) for j in range(42,48)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(42,44) for j in range(44,48)]
            map.extend(add)   
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(44,48)]
            map.extend(add)   
            return {'x1':8, 'x2':47, 'y1':6, 'y2':47}, map 
               
        # Map isle_snow2   Полярной ночи, НЛО, Лысая гора, Большой ёлки, Лунный
        if(ostrov in ['isle_polar', 'isle_ufo', 'isle_halloween', 'isle_large', 'isle_moon']):
            map = [ str(i)+''+str(j) for i in range(8,12) for j in range(6,10)]
            add = [ str(i)+''+str(j) for i in range(8,10) for j in range(44,48)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,48) for j in range(44,48)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,48) for j in range(42,44)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(42,48) for j in range(6,8)]
            map.extend(add)
            add = [ str(i)+''+str(j) for i in range(44,48) for j in range(8,10)]
            map.extend(add)             
            return {'x1':8, 'x2':47, 'y1':6, 'y2':47}, map 
