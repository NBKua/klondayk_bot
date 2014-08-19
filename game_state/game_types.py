from mixins import CommonEqualityMixin
from types import NoneType


class GameAction(CommonEqualityMixin):
    pass


class GameAddPickup(GameAction):
    type = 'pickup'

    def __init__(self, pickups=None):  # @ReservedAssignment
        assert (pickups is None
                or isinstance(pickups, list))
        self.action = 'add'
        self.pickups = pickups
        self.type = 'pickup'


class GameApplyCompGiftItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 extraId=None,  # @ReservedAssignment
                 objId=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (extraId is None
                or isinstance(extraId, long))
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.action = 'applyCompGift'
        self.extraId = extraId
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'
        self.x = x
        self.y = y


class GameApplyGiftEvent(GameAction):
    type = 'gift'

    def __init__(self, gift=None):  # @ReservedAssignment
        assert (gift is None
                or isinstance(gift, GameGift))
        self.action = 'applyGift'
        self.gift = gift
        self.type = 'gift'


class GameBuffs(CommonEqualityMixin):
    def __init__(self, list=None):  # @ReservedAssignment
        assert (list is None
                or isinstance(list, list))
        self.list = list


class GameBurySlot(CommonEqualityMixin):
    def __init__(self, enabled=None):
        assert (enabled is None
                or isinstance(enabled, bool))
        self.enabled = enabled


class GameBuyItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.action = 'buy'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'
        self.x = x
        self.y = y


class GameCollectionItems(CommonEqualityMixin):
    def __init__(self, C_18_2=None,
                 C_4_3=None,
                 C_18_1=None,
                 C_13_3=None,
                 C_4_4=None,
                 C_18_3=None,
                 C_19_3=None,
                 C_19_2=None,
                 C_19_1=None,
                 C_19_5=None,
                 C_37_2=None,
                 C_3_1=None,
                 C_30_5=None,
                 C_3_3=None,
                 C_3_2=None,
                 C_3_5=None,
                 C_9_4=None,
                 C_5_2=None,
                 C_2_1=None,
                 C_5_1=None,
                 C_2_3=None,
                 C_31_1=None,
                 C_2_5=None,
                 C_5_5=None,
                 C_31_2=None,
                 C_15_5=None,
                 C_1_4=None,
                 C_1_3=None,
                 C_8_3=None,
                 C_15_1=None,
                 C_12_5=None,
                 C_4_1=None,
                 C_4_5=None,
                 C_20_1=None,
                 C_12_1=None,
                 C_12_3=None,
                 C_17_1=None,
                 C_10_2=None,
                 C_31_3=None,
                 C_4_2=None,
                 C_7_2=None,
                 C_6_4=None,
                 C_6_5=None,
                 C_14_4=None,
                 C_10_5=None,
                 C_14_2=None,
                 C_6_1=None,
                 C_2_2=None,
                 C_6_3=None,
                 C_11_3=None,
                 C_21_3=None,
                 C_16_2=None,
                 C_16_4=None,
                 C_15_3=None,
                 C_20_3=None,
                 C_20_2=None,
                 C_17_3=None,
                 C_17_5=None,
                 C_8_4=None,
                 C_17_4=None,
                 C_13_4=None,
                 C_5_4=None,
                 C_23_2=None,
                 C_13_2=None,
                 C_22_5=None,
                 C_10_3=None,
                 C_20_4=None,
                 C_15_2=None,
                 C_10_4=None,
                 C_22_2=None,
                 C_25_4=None,
                 C_14_5=None,
                 C_25_2=None,
                 C_25_1=None,
                 C_24_5=None,
                 C_24_4=None,
                 C_24_2=None,
                 C_24_1=None,
                 C_9_2=None,
                 C_9_1=None,
                 C_6_2=None,
                 C_29_3=None,
                 C_14_1=None,
                 C_1_2=None):
        assert (C_10_2 is None
                or isinstance(C_10_2, long))
        assert (C_10_3 is None
                or isinstance(C_10_3, long))
        assert (C_10_4 is None
                or isinstance(C_10_4, long))
        assert (C_10_5 is None
                or isinstance(C_10_5, long))
        assert (C_11_3 is None
                or isinstance(C_11_3, long))
        assert (C_12_1 is None
                or isinstance(C_12_1, long))
        assert (C_12_3 is None
                or isinstance(C_12_3, long))
        assert (C_12_5 is None
                or isinstance(C_12_5, long))
        assert (C_13_2 is None
                or isinstance(C_13_2, long))
        assert (C_13_3 is None
                or isinstance(C_13_3, long))
        assert (C_13_4 is None
                or isinstance(C_13_4, long))
        assert (C_14_1 is None
                or isinstance(C_14_1, long))
        assert (C_14_2 is None
                or isinstance(C_14_2, long))
        assert (C_14_4 is None
                or isinstance(C_14_4, long))
        assert (C_14_5 is None
                or isinstance(C_14_5, long))
        assert (C_15_1 is None
                or isinstance(C_15_1, long))
        assert (C_15_2 is None
                or isinstance(C_15_2, long))
        assert (C_15_3 is None
                or isinstance(C_15_3, long))
        assert (C_15_5 is None
                or isinstance(C_15_5, long))
        assert (C_16_2 is None
                or isinstance(C_16_2, long))
        assert (C_16_4 is None
                or isinstance(C_16_4, long))
        assert (C_17_1 is None
                or isinstance(C_17_1, long))
        assert (C_17_3 is None
                or isinstance(C_17_3, long))
        assert (C_17_4 is None
                or isinstance(C_17_4, long))
        assert (C_17_5 is None
                or isinstance(C_17_5, long))
        assert (C_18_1 is None
                or isinstance(C_18_1, long))
        assert (C_18_2 is None
                or isinstance(C_18_2, long))
        assert (C_18_3 is None
                or isinstance(C_18_3, long))
        assert (C_19_1 is None
                or isinstance(C_19_1, long))
        assert (C_19_2 is None
                or isinstance(C_19_2, long))
        assert (C_19_3 is None
                or isinstance(C_19_3, long))
        assert (C_19_5 is None
                or isinstance(C_19_5, long))
        assert (C_1_2 is None
                or isinstance(C_1_2, long))
        assert (C_1_3 is None
                or isinstance(C_1_3, long))
        assert (C_1_4 is None
                or isinstance(C_1_4, long))
        assert (C_20_1 is None
                or isinstance(C_20_1, long))
        assert (C_20_2 is None
                or isinstance(C_20_2, long))
        assert (C_20_3 is None
                or isinstance(C_20_3, long))
        assert (C_20_4 is None
                or isinstance(C_20_4, long))
        assert (C_21_3 is None
                or isinstance(C_21_3, long))
        assert (C_22_2 is None
                or isinstance(C_22_2, long))
        assert (C_22_5 is None
                or isinstance(C_22_5, long))
        assert (C_23_2 is None
                or isinstance(C_23_2, long))
        assert (C_24_1 is None
                or isinstance(C_24_1, long))
        assert (C_24_2 is None
                or isinstance(C_24_2, long))
        assert (C_24_4 is None
                or isinstance(C_24_4, long))
        assert (C_24_5 is None
                or isinstance(C_24_5, long))
        assert (C_25_1 is None
                or isinstance(C_25_1, long))
        assert (C_25_2 is None
                or isinstance(C_25_2, long))
        assert (C_25_4 is None
                or isinstance(C_25_4, long))
        assert (C_29_3 is None
                or isinstance(C_29_3, long))
        assert (C_2_1 is None
                or isinstance(C_2_1, long))
        assert (C_2_2 is None
                or isinstance(C_2_2, long))
        assert (C_2_3 is None
                or isinstance(C_2_3, long))
        assert (C_2_5 is None
                or isinstance(C_2_5, long))
        assert (C_30_5 is None
                or isinstance(C_30_5, long))
        assert (C_31_1 is None
                or isinstance(C_31_1, long))
        assert (C_31_2 is None
                or isinstance(C_31_2, long))
        assert (C_31_3 is None
                or isinstance(C_31_3, long))
        assert (C_37_2 is None
                or isinstance(C_37_2, long))
        assert (C_3_1 is None
                or isinstance(C_3_1, long))
        assert (C_3_2 is None
                or isinstance(C_3_2, long))
        assert (C_3_3 is None
                or isinstance(C_3_3, long))
        assert (C_3_5 is None
                or isinstance(C_3_5, long))
        assert (C_4_1 is None
                or isinstance(C_4_1, long))
        assert (C_4_2 is None
                or isinstance(C_4_2, long))
        assert (C_4_3 is None
                or isinstance(C_4_3, long))
        assert (C_4_4 is None
                or isinstance(C_4_4, long))
        assert (C_4_5 is None
                or isinstance(C_4_5, long))
        assert (C_5_1 is None
                or isinstance(C_5_1, long))
        assert (C_5_2 is None
                or isinstance(C_5_2, long))
        assert (C_5_4 is None
                or isinstance(C_5_4, long))
        assert (C_5_5 is None
                or isinstance(C_5_5, long))
        assert (C_6_1 is None
                or isinstance(C_6_1, long))
        assert (C_6_2 is None
                or isinstance(C_6_2, long))
        assert (C_6_3 is None
                or isinstance(C_6_3, long))
        assert (C_6_4 is None
                or isinstance(C_6_4, long))
        assert (C_6_5 is None
                or isinstance(C_6_5, long))
        assert (C_7_2 is None
                or isinstance(C_7_2, long))
        assert (C_8_3 is None
                or isinstance(C_8_3, long))
        assert (C_8_4 is None
                or isinstance(C_8_4, long))
        assert (C_9_1 is None
                or isinstance(C_9_1, long))
        assert (C_9_2 is None
                or isinstance(C_9_2, long))
        assert (C_9_4 is None
                or isinstance(C_9_4, long))
        self.C_10_2 = C_10_2
        self.C_10_3 = C_10_3
        self.C_10_4 = C_10_4
        self.C_10_5 = C_10_5
        self.C_11_3 = C_11_3
        self.C_12_1 = C_12_1
        self.C_12_3 = C_12_3
        self.C_12_5 = C_12_5
        self.C_13_2 = C_13_2
        self.C_13_3 = C_13_3
        self.C_13_4 = C_13_4
        self.C_14_1 = C_14_1
        self.C_14_2 = C_14_2
        self.C_14_4 = C_14_4
        self.C_14_5 = C_14_5
        self.C_15_1 = C_15_1
        self.C_15_2 = C_15_2
        self.C_15_3 = C_15_3
        self.C_15_5 = C_15_5
        self.C_16_2 = C_16_2
        self.C_16_4 = C_16_4
        self.C_17_1 = C_17_1
        self.C_17_3 = C_17_3
        self.C_17_4 = C_17_4
        self.C_17_5 = C_17_5
        self.C_18_1 = C_18_1
        self.C_18_2 = C_18_2
        self.C_18_3 = C_18_3
        self.C_19_1 = C_19_1
        self.C_19_2 = C_19_2
        self.C_19_3 = C_19_3
        self.C_19_5 = C_19_5
        self.C_1_2 = C_1_2
        self.C_1_3 = C_1_3
        self.C_1_4 = C_1_4
        self.C_20_1 = C_20_1
        self.C_20_2 = C_20_2
        self.C_20_3 = C_20_3
        self.C_20_4 = C_20_4
        self.C_21_3 = C_21_3
        self.C_22_2 = C_22_2
        self.C_22_5 = C_22_5
        self.C_23_2 = C_23_2
        self.C_24_1 = C_24_1
        self.C_24_2 = C_24_2
        self.C_24_4 = C_24_4
        self.C_24_5 = C_24_5
        self.C_25_1 = C_25_1
        self.C_25_2 = C_25_2
        self.C_25_4 = C_25_4
        self.C_29_3 = C_29_3
        self.C_2_1 = C_2_1
        self.C_2_2 = C_2_2
        self.C_2_3 = C_2_3
        self.C_2_5 = C_2_5
        self.C_30_5 = C_30_5
        self.C_31_1 = C_31_1
        self.C_31_2 = C_31_2
        self.C_31_3 = C_31_3
        self.C_37_2 = C_37_2
        self.C_3_1 = C_3_1
        self.C_3_2 = C_3_2
        self.C_3_3 = C_3_3
        self.C_3_5 = C_3_5
        self.C_4_1 = C_4_1
        self.C_4_2 = C_4_2
        self.C_4_3 = C_4_3
        self.C_4_4 = C_4_4
        self.C_4_5 = C_4_5
        self.C_5_1 = C_5_1
        self.C_5_2 = C_5_2
        self.C_5_4 = C_5_4
        self.C_5_5 = C_5_5
        self.C_6_1 = C_6_1
        self.C_6_2 = C_6_2
        self.C_6_3 = C_6_3
        self.C_6_4 = C_6_4
        self.C_6_5 = C_6_5
        self.C_7_2 = C_7_2
        self.C_8_3 = C_8_3
        self.C_8_4 = C_8_4
        self.C_9_1 = C_9_1
        self.C_9_2 = C_9_2
        self.C_9_4 = C_9_4


class GameDailyBonus(CommonEqualityMixin):
    def __init__(self, dayItemses=None,
                 current=None,
                 playFrom=None,
                 prizes=None):
        assert (current is None
                or isinstance(current, long))
        assert (dayItemses is None
                or isinstance(dayItemses, list))
        assert (playFrom is None
                or isinstance(playFrom, unicode))
        assert (prizes is None
                or isinstance(prizes, list))
        self.current = current
        self.dayItemses = dayItemses
        self.playFrom = playFrom
        self.prizes = prizes


class GameDigItem(GameAction):
    type = 'item'

    def __init__(self, objId=None):  # @ReservedAssignment
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'dig'
        self.objId = objId
        self.type = 'item'


class GameStartTimeGainEvent(GameAction):
    type = 'timeGain'

    def __init__(self, objId=None, gainDone=None):
        assert (objId is None
                or isinstance(objId, long))
        assert (gainDone is None
                or isinstance(gainDone, long))
        self.action = 'start'
        self.objId = objId
        self.gainDone = gainDone


class GameEVTCommand(CommonEqualityMixin):
    def __init__(self, id=None,  # @ReservedAssignment
                 events=None):  # @ReservedAssignment
        assert (events is None
                or isinstance(events, list))
        assert (id is None
                or isinstance(id, unicode))
        self.cmd = 'EVT'
        self.events = events
        self.id = id


class GameFertilizePlant(GameAction):
    type = 'plant'

    def __init__(self, jobFinishTime=None,  # @ReservedAssignment
                 jobStartTime=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (jobFinishTime is None
                or isinstance(jobFinishTime, unicode))
        assert (jobStartTime is None
                or isinstance(jobStartTime, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'fertilize'
        self.jobFinishTime = jobFinishTime
        self.jobStartTime = jobStartTime
        self.objId = objId
        self.type = 'plant'


class GameGainItem(GameAction):
    type = 'item'

    def __init__(self, objId=None,  # @ReservedAssignment
                 extraId=None):  # @ReservedAssignment
        assert (extraId is None
                or isinstance(extraId, long))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'gain'
        self.extraId = extraId
        self.objId = objId
        self.type = 'item'


class GameGameSettings(CommonEqualityMixin):
    def __init__(self, sound=None,
                 tutorialState=None,
                 music=None):
        assert (music is None
                or isinstance(music, bool))
        assert (sound is None
                or isinstance(sound, bool))
        assert (tutorialState is None
                or isinstance(tutorialState, long))
        self.music = music
        self.sound = sound
        self.tutorialState = tutorialState


class GameGameStateEvent(GameAction):
    type = 'gameState'

    def __init__(self, isAway=None,  # @ReservedAssignment
                 haveTrickTreating=None,  # @ReservedAssignment
                 haveTreasure=None,  # @ReservedAssignment
                 wishlist=None,  # @ReservedAssignment
                 haveAttempts=None,  # @ReservedAssignment
                 haveRemoteFertilizeFruit=None,  # @ReservedAssignment
                 locationInfos=None,  # @ReservedAssignment
                 locationId=None,  # @ReservedAssignment
                 location=None,  # @ReservedAssignment
                 playerSettings=None,  # @ReservedAssignment
                 playerStatus=None,  # @ReservedAssignment
                 treasureRehide=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 haveThanksgivingAttempt=None):  # @ReservedAssignment
        assert (haveAttempts is None
                or isinstance(haveAttempts, bool))
        assert (haveRemoteFertilizeFruit is None
                or isinstance(haveRemoteFertilizeFruit, bool))
        assert (haveThanksgivingAttempt is None
                or isinstance(haveThanksgivingAttempt, bool))
        assert (haveTreasure is None
                or isinstance(haveTreasure, bool))
        assert (haveTrickTreating is None
                or isinstance(haveTrickTreating, bool))
        assert (id is None
                or isinstance(id, unicode))
        assert (isAway is None
                or isinstance(isAway, bool))
        assert (location is None
                or isinstance(location, GameLocation))
        assert (locationId is None
                or isinstance(locationId, unicode))
        assert (locationInfos is None
                or isinstance(locationInfos, list))
        assert (playerSettings is None
                or isinstance(playerSettings, GamePlayerSettings))
        assert (playerStatus is None
                or isinstance(playerStatus, unicode))
        assert (treasureRehide is None
                or isinstance(treasureRehide, long))
        assert (wishlist is None
                or isinstance(wishlist, list))
        self.action = 'gameState'
        self.haveAttempts = haveAttempts
        self.haveRemoteFertilizeFruit = haveRemoteFertilizeFruit
        self.haveThanksgivingAttempt = haveThanksgivingAttempt
        self.haveTreasure = haveTreasure
        self.haveTrickTreating = haveTrickTreating
        self.id = id
        self.isAway = isAway
        self.location = location
        self.locationId = locationId
        self.locationInfos = locationInfos
        self.playerSettings = playerSettings
        self.playerStatus = playerStatus
        self.treasureRehide = treasureRehide
        self.type = 'gameState'
        self.wishlist = wishlist


class GameGetMissionsMission(GameAction):
    type = 'mission'

    def __init__(self, id=None,  # @ReservedAssignment
                 missions=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, unicode))
        assert (missions is None
                or isinstance(missions, list))
        self.action = 'getMissions'
        self.id = id
        self.missions = missions
        self.type = 'mission'


class GameGift(CommonEqualityMixin):
    def __init__(self, id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        self.id = id


class GameGuestInfo(CommonEqualityMixin):
    def __init__(self, visitingTime=None,
                 userId=None,
                 playerSettings=None):
        assert (playerSettings is None
                or isinstance(playerSettings, GamePlayerSettings))
        assert (userId is None
                or isinstance(userId, unicode))
        assert (visitingTime is None
                or isinstance(visitingTime, long))
        self.playerSettings = playerSettings
        self.userId = userId
        self.visitingTime = visitingTime


class GameInfo(CommonEqualityMixin):
    def __init__(self, city=None,
                 first_name=None,
                 last_name=None,
                 uid=None,
                 country=None,
                 sex=None,
                 bdate=None):
        assert (bdate is None
                or isinstance(bdate, unicode))
        assert (city is None
                or isinstance(city, unicode))
        assert (country is None
                or isinstance(country, unicode))
        assert (first_name is None
                or isinstance(first_name, unicode))
        assert (last_name is None
                or isinstance(last_name, unicode))
        assert (sex is None
                or isinstance(sex, long))
        assert (uid is None
                or isinstance(uid, long))
        self.bdate = bdate
        self.city = city
        self.country = country
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.uid = uid


class GameItem(CommonEqualityMixin):
    pass


class GameLocation(GameItem):
    def __init__(self, width=None,  # @ReservedAssignment
                 openedAreas=None,  # @ReservedAssignment
                 height=None,  # @ReservedAssignment
                 gameObjects=None,  # @ReservedAssignment
                 guestInfos=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gameObjects is None
                or isinstance(gameObjects, list))
        assert (guestInfos is None
                or isinstance(guestInfos, list))
        assert (height is None
                or isinstance(height, long))
        assert (id is None
                or isinstance(id, unicode))
        assert (openedAreas is None
                or isinstance(openedAreas, list))
        assert (width is None
                or isinstance(width, long))
        self.gameObjects = gameObjects
        self.guestInfos = guestInfos
        self.height = height
        self.id = id
        self.item = '@isle_03'
        self.openedAreas = openedAreas
        self.width = width


class GameLocationInfo(CommonEqualityMixin):
    def __init__(self, openedAreas=None,
                 occupiedBrainsCount=None,
                 locationId=None,
                 maxGameObjectId=None,
                 giftCoins=None):
        assert (giftCoins is None
                or isinstance(giftCoins, long))
        assert (locationId is None
                or isinstance(locationId, unicode))
        assert (maxGameObjectId is None
                or isinstance(maxGameObjectId, long))
        assert (occupiedBrainsCount is None
                or isinstance(occupiedBrainsCount, long))
        assert (openedAreas is None
                or isinstance(openedAreas, list))
        self.giftCoins = giftCoins
        self.locationId = locationId
        self.maxGameObjectId = maxGameObjectId
        self.occupiedBrainsCount = occupiedBrainsCount
        self.openedAreas = openedAreas


class GameMagic(CommonEqualityMixin):
    def __init__(self, expire=None,
                 used=None):
        assert (expire is None
                or isinstance(expire, unicode))
        assert (used is None
                or isinstance(used, long))
        self.expire = expire
        self.used = used


class GameMailBonus(CommonEqualityMixin):
    def __init__(self, bonuses=None,
                 acceptedBonuses=None):
        assert (acceptedBonuses is None
                or isinstance(acceptedBonuses, list))
        assert (bonuses is None
                or isinstance(bonuses, list))
        self.acceptedBonuses = acceptedBonuses
        self.bonuses = bonuses


class GameMoveToStorageItem(GameAction):
    type = 'item'

    def __init__(self, objId=None):  # @ReservedAssignment
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'moveToStorage'
        self.objId = objId
        self.type = 'item'


class GameNextPlayTimes(CommonEqualityMixin):
    pass


class GameNpcs(CommonEqualityMixin):
    def __init__(self, npcClientId=None):
        assert (npcClientId is None
                or isinstance(npcClientId, long))
        self.npcClientId = npcClientId


class GameParams(CommonEqualityMixin):
    def __init__(self, magicLimit=None,
                 event=None):
        assert (event is None
                or isinstance(event, GameGameStateEvent))
        assert (magicLimit is None
                or isinstance(magicLimit, long))
        self.event = event
        self.magicLimit = magicLimit


class GamePickItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'pick'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'


class GamePickPickup(GameAction):
    type = 'pickup'

    def __init__(self, pickups=None):  # @ReservedAssignment
        assert (pickups is None
                or isinstance(pickups, list))
        self.action = 'pick'
        self.pickups = pickups
        self.type = 'pickup'


class GamePlayGame(GameAction):
    type = 'game'

    def __init__(self, objId=None,  # @ReservedAssignment
                 extraId=None):  # @ReservedAssignment
        assert (extraId is None
                or isinstance(extraId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'play'
        self.extraId = extraId
        self.objId = objId
        self.type = 'game'


class GamePlayerSettings(CommonEqualityMixin):
    def __init__(self, userName=None,
                 dressId=None,
                 hatId=None):
        assert (dressId is None
                or isinstance(dressId, unicode))
        assert (hatId is None
                or isinstance(hatId, unicode))
        assert (userName is None
                or isinstance(userName, unicode))
        self.dressId = dressId
        self.hatId = hatId
        self.userName = userName


class GamePresent(GameItem):
    def __init__(self, count=None):
        assert (count is None
                or isinstance(count, long))
        self.count = count
        self.item = '@CR_112'


class GamePrize(GameItem):
    def __init__(self, count=None):
        assert (count is None
                or isinstance(count, long))
        self.count = count
        self.item = '@CR_07'


class GameRemoteNewYearItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'remoteNewYear'
        self.id = id
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'


class GameSTARTCommand(CommonEqualityMixin):
    def __init__(self, state=None,  # @ReservedAssignment
                 params=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, unicode))
        assert (params is None
                or isinstance(params, GameParams))
        assert (state is None
                or isinstance(state, GameState))
        self.cmd = 'START'
        self.id = id
        self.params = params
        self.state = state


class GameStartGainMaterial(GameAction):
    type = 'gainMaterial'

    def __init__(self, targetId=None,  # @ReservedAssignment
                 startCounter=None,  # @ReservedAssignment
                 jobStartTime=None,  # @ReservedAssignment
                 objId=None,  # @ReservedAssignment
                 doneCounter=None,  # @ReservedAssignment
                 jobEndTime=None):  # @ReservedAssignment
        assert (doneCounter is None
                or isinstance(doneCounter, long))
        assert (jobEndTime is None
                or isinstance(jobEndTime, unicode))
        assert (jobStartTime is None
                or isinstance(jobStartTime, unicode))
        assert (objId is None
                or isinstance(objId, long))
        assert (startCounter is None
                or isinstance(startCounter, long))
        assert (targetId is None
                or isinstance(targetId, long))
        self.action = 'start'
        self.doneCounter = doneCounter
        self.jobEndTime = jobEndTime
        self.jobStartTime = jobStartTime
        self.objId = objId
        self.startCounter = startCounter
        self.targetId = targetId
        self.type = 'gainMaterial'


class GameState(CommonEqualityMixin):
    def __init__(self, gameSettings=None,
                 cashMoneyReal=None,
                 definedBonuses=None,
                 treasureHide=None,
                 cashMoney=None,
                 remoteNewYearExpire=None,
                 gameMoneyReal=None,
                 storageItems=None,
                 buyedClothing=None,
                 mailBonus=None,
                 playerSettings=None,
                 dailyBonus=None,
                 gameMoney=None,
                 buffs=None,
                 remoteTrickTreating=None,
                 buyedBrains=None,
                 treasureExpire=None,
                 treasureCount=None,
                 burySlots=None,
                 collectionItems=None,
                 gifts=None,
                 freeGiftUsers=None,
                 remoteTreasure=None,
                 receivedGiftsExpire=None,
                 wishlist=None,
                 remoteNewYear=None,
                 brainsCount=None,
                 npcs=None,
                 magic=None,
                 storageGameObjects=None,
                 remoteFertilizeFruitTree=None,
                 receivedGiftsCoins=None,
                 level=None,
                 remoteFertilizeFruitTreeCount=None,
                 experience=None,
                 giftId=None,
                 retentionBonuses=None,
                 playerStatus=None,
                 registerDate=None,
                 remoteThanksgiving=None,
                 shopOpened=None):
        assert (brainsCount is None
                or isinstance(brainsCount, long))
        assert (buffs is None
                or isinstance(buffs, GameBuffs))
        assert (burySlots is None
                or isinstance(burySlots, list))
        assert (buyedBrains is None
                or isinstance(buyedBrains, list))
        assert (buyedClothing is None
                or isinstance(buyedClothing, list))
        assert (cashMoney is None
                or isinstance(cashMoney, long))
        assert (cashMoneyReal is None
                or isinstance(cashMoneyReal, long))
        assert (collectionItems is None
                or isinstance(collectionItems, GameCollectionItems))
        assert (dailyBonus is None
                or isinstance(dailyBonus, GameDailyBonus))
        assert (definedBonuses is None
                or isinstance(definedBonuses, list))
        assert (experience is None
                or isinstance(experience, long))
        assert (freeGiftUsers is None
                or isinstance(freeGiftUsers, list))
        assert (gameMoney is None
                or isinstance(gameMoney, long))
        assert (gameMoneyReal is None
                or isinstance(gameMoneyReal, long))
        assert (gameSettings is None
                or isinstance(gameSettings, GameGameSettings))
        assert (giftId is None
                or isinstance(giftId, long))
        assert (gifts is None
                or isinstance(gifts, list))
        assert (level is None
                or isinstance(level, long))
        assert (magic is None
                or isinstance(magic, GameMagic))
        assert (mailBonus is None
                or isinstance(mailBonus, GameMailBonus))
        assert (npcs is None
                or isinstance(npcs, GameNpcs))
        assert (playerSettings is None
                or isinstance(playerSettings, GamePlayerSettings))
        assert (playerStatus is None
                or isinstance(playerStatus, unicode))
        assert (receivedGiftsCoins is None
                or isinstance(receivedGiftsCoins, long))
        assert (receivedGiftsExpire is None
                or isinstance(receivedGiftsExpire, unicode))
        assert (registerDate is None
                or isinstance(registerDate, unicode))
        assert (remoteFertilizeFruitTree is None
                or isinstance(remoteFertilizeFruitTree, list))
        assert (remoteFertilizeFruitTreeCount is None
                or isinstance(remoteFertilizeFruitTreeCount, long))
        assert (remoteNewYear is None
                or isinstance(remoteNewYear, list))
        assert (remoteNewYearExpire is None
                or isinstance(remoteNewYearExpire, unicode))
        assert (remoteThanksgiving is None
                or isinstance(remoteThanksgiving, list))
        assert (remoteTreasure is None
                or isinstance(remoteTreasure, list))
        assert (remoteTrickTreating is None
                or isinstance(remoteTrickTreating, list))
        assert (retentionBonuses is None
                or isinstance(retentionBonuses, bool))
        assert (shopOpened is None
                or isinstance(shopOpened, list))
        assert (storageGameObjects is None
                or isinstance(storageGameObjects, list))
        assert (storageItems is None
                or isinstance(storageItems, list))
        assert (treasureCount is None
                or isinstance(treasureCount, long))
        assert (treasureExpire is None
                or isinstance(treasureExpire, unicode))
        assert (treasureHide is None
                or isinstance(treasureHide, unicode))
        assert (wishlist is None
                or isinstance(wishlist, list))
        self.brainsCount = brainsCount
        self.buffs = buffs
        self.burySlots = burySlots
        self.buyedBrains = buyedBrains
        self.buyedClothing = buyedClothing
        self.cashMoney = cashMoney
        self.cashMoneyReal = cashMoneyReal
        self.collectionItems = collectionItems
        self.dailyBonus = dailyBonus
        self.definedBonuses = definedBonuses
        self.experience = experience
        self.freeGiftUsers = freeGiftUsers
        self.gameMoney = gameMoney
        self.gameMoneyReal = gameMoneyReal
        self.gameSettings = gameSettings
        self.giftId = giftId
        self.gifts = gifts
        self.level = level
        self.magic = magic
        self.mailBonus = mailBonus
        self.npcs = npcs
        self.playerSettings = playerSettings
        self.playerStatus = playerStatus
        self.receivedGiftsCoins = receivedGiftsCoins
        self.receivedGiftsExpire = receivedGiftsExpire
        self.registerDate = registerDate
        self.remoteFertilizeFruitTree = remoteFertilizeFruitTree
        self.remoteFertilizeFruitTreeCount = remoteFertilizeFruitTreeCount
        self.remoteNewYear = remoteNewYear
        self.remoteNewYearExpire = remoteNewYearExpire
        self.remoteThanksgiving = remoteThanksgiving
        self.remoteTreasure = remoteTreasure
        self.remoteTrickTreating = remoteTrickTreating
        self.retentionBonuses = retentionBonuses
        self.shopOpened = shopOpened
        self.storageGameObjects = storageGameObjects
        self.storageItems = storageItems
        self.treasureCount = treasureCount
        self.treasureExpire = treasureExpire
        self.treasureHide = treasureHide
        self.wishlist = wishlist


class GameStorageGameObject(GameItem):
    def __init__(self, count=None):
        assert (count is None
                or isinstance(count, long))
        self.count = count
        self.item = '@SC_WOOD_GRAVE2'


class GameStorageItem(GameItem):
    def __init__(self, count=None):
        assert (count is None
                or isinstance(count, long))
        self.count = count
        self.item = '@METAL_SCRAP'


class GameTarget(CommonEqualityMixin):
    def __init__(self, id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        self.id = id


class GameTasks(CommonEqualityMixin):
    def __init__(self, Q15_11_T2=None,
                 Q15_11_T3=None,
                 Q15_11_T1=None):
        assert (Q15_11_T1 is None
                or isinstance(Q15_11_T1, GameCountedItem))
        assert (Q15_11_T2 is None
                or isinstance(Q15_11_T2, GameCountedItem))
        assert (Q15_11_T3 is None
                or isinstance(Q15_11_T3, GameCountedItem))
        self.Q15_11_T1 = Q15_11_T1
        self.Q15_11_T2 = Q15_11_T2
        self.Q15_11_T3 = Q15_11_T3


class GameType(CommonEqualityMixin):
    pass


class GameUpgradeBuilding(GameType):
    type = 'upgradeBuilding'

    def __init__(self, count=None,  # @ReservedAssignment
                 finished=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (finished is None
                or isinstance(finished, bool))
        self.count = count
        self.finished = finished
        self.type = 'upgradeBuilding'


class GameUser(CommonEqualityMixin):
    def __init__(self, id=None,  # @ReservedAssignment
                 present=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, unicode))
        assert (present is None
                or isinstance(present, GamePresent))
        self.id = id
        self.present = present


class GameWoodGrave(GameType):
    type = 'woodGrave'

    def __init__(self, target=None,  # @ReservedAssignment
                 startCounter=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 doneCounter=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (doneCounter is None
                or isinstance(doneCounter, long))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, list))
        assert (startCounter is None
                or isinstance(startCounter, long))
        assert (target is None
                or isinstance(target, NoneType))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.doneCounter = doneCounter
        self.id = id
        self.item = '@SC_WOOD_GRAVE'
        self.materials = materials
        self.startCounter = startCounter
        self.target = target
        self.type = 'woodGrave'
        self.x = x
        self.y = y


class GameWoodGraveDouble(GameType):
    type = 'woodGraveDouble'

    def __init__(self, target=None,  # @ReservedAssignment
                 startCounter=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 doneCounter=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (doneCounter is None
                or isinstance(doneCounter, long))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, list))
        assert (startCounter is None
                or isinstance(startCounter, long))
        assert (target is None
                or isinstance(target, GameTarget))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.doneCounter = doneCounter
        self.id = id
        self.item = '@SC_WOOD_GRAVE2'
        self.materials = materials
        self.startCounter = startCounter
        self.target = target
        self.type = 'woodGraveDouble'
        self.x = x
        self.y = y


class GameWoodTree(GameType):
    type = 'woodTree'

    def __init__(self, materialCount=None,  # @ReservedAssignment
                 gainStarted=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainStarted is None
                or isinstance(gainStarted, bool))
        assert (id is None
                or isinstance(id, long))
        assert (materialCount is None
                or isinstance(materialCount, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainStarted = gainStarted
        self.id = id
        self.item = '@SC_OAK6'
        self.materialCount = materialCount
        self.type = 'woodTree'
        self.x = x
        self.y = y


class GameXp(GameType):
    type = 'xp'

    def __init__(self, count=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 y=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.count = count
        self.type = 'xp'
        self.x = x
        self.y = y


class GameZombieWork(GameType):
    type = 'zombieWork'

    def __init__(self, count=None,  # @ReservedAssignment
                 finished=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (finished is None
                or isinstance(finished, bool))
        self.count = count
        self.finished = finished
        self.type = 'zombieWork'


class GameADMIN(GameType):
    type = 'ADMIN'

    def __init__(self, count=None,  # @ReservedAssignment
                 free=None,  # @ReservedAssignment
                 user=None,  # @ReservedAssignment
                 msg=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (free is None
                or isinstance(free, bool))
        assert (id is None
                or isinstance(id, long))
        assert (msg is None
                or isinstance(msg, unicode))
        assert (user is None
                or isinstance(user, unicode))
        self.count = count
        self.free = free
        self.id = id
        self.item = '@BELL'
        self.msg = msg
        self.type = 'ADMIN'
        self.user = user


class GameBase(GameType):
    type = 'base'

    def __init__(self, y=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@D_FENCE1'
        self.type = 'base'
        self.x = x
        self.y = y


class GameBridge(GameType):
    type = 'bridge'

    def __init__(self, level=None,  # @ReservedAssignment
                 nextPlayTimes=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (level is None
                or isinstance(level, long))
        assert (nextPlayTimes is None
                or isinstance(nextPlayTimes, GameNextPlayTimes))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_BRIDGE'
        self.level = level
        self.nextPlayTimes = nextPlayTimes
        self.type = 'bridge'
        self.x = x
        self.y = y


class GameBuilding(GameType):
    type = 'building'

    def __init__(self, level=None,  # @ReservedAssignment
                 nextPlayTimes=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (level is None
                or isinstance(level, long))
        assert (nextPlayTimes is None
                or isinstance(nextPlayTimes, GameNextPlayTimes))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_FLAG_EMERALD'
        self.level = level
        self.nextPlayTimes = nextPlayTimes
        self.type = 'building'
        self.x = x
        self.y = y


class GameCoins(GameType):
    type = 'coins'

    def __init__(self, count=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 y=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.count = count
        self.type = 'coins'
        self.x = x
        self.y = y


class GameCollection(GameType):
    type = 'collection'

    def __init__(self, count=None,  # @ReservedAssignment
                 img=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (id is None
                or isinstance(id, unicode))
        assert (img is None
                or isinstance(img, unicode))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.count = count
        self.id = id
        self.img = img
        self.type = 'collection'
        self.x = x
        self.y = y


class GameCookGrave(GameType):
    type = 'cookGrave'

    def __init__(self, jobEndTime=None,  # @ReservedAssignment
                 speeduped=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 isUp=None,  # @ReservedAssignment
                 recipeNo=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 pendingRecipes=None,  # @ReservedAssignment
                 currentRecipe=None):  # @ReservedAssignment
        assert (currentRecipe is None
                or isinstance(currentRecipe, unicode))
        assert (id is None
                or isinstance(id, long))
        assert (isUp is None
                or isinstance(isUp, bool))
        assert (jobEndTime is None
                or isinstance(jobEndTime, unicode))
        assert (materials is None
                or isinstance(materials, list))
        assert (pendingRecipes is None
                or isinstance(pendingRecipes, list))
        assert (recipeNo is None
                or isinstance(recipeNo, long))
        assert (speeduped is None
                or isinstance(speeduped, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.currentRecipe = currentRecipe
        self.id = id
        self.isUp = isUp
        self.item = '@SC_COOK_GRAVE'
        self.jobEndTime = jobEndTime
        self.materials = materials
        self.pendingRecipes = pendingRecipes
        self.recipeNo = recipeNo
        self.speeduped = speeduped
        self.type = 'cookGrave'
        self.x = x
        self.y = y


class GameCookGraveWithBrains(GameType):
    type = 'cookGraveWithBrains'

    def __init__(self, speeduped=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 isUp=None,  # @ReservedAssignment
                 recipeNo=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 pendingRecipes=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (isUp is None
                or isinstance(isUp, bool))
        assert (materials is None
                or isinstance(materials, list))
        assert (pendingRecipes is None
                or isinstance(pendingRecipes, list))
        assert (recipeNo is None
                or isinstance(recipeNo, long))
        assert (speeduped is None
                or isinstance(speeduped, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.isUp = isUp
        self.item = '@SC_COOK_GRAVE_BRAINER'
        self.materials = materials
        self.pendingRecipes = pendingRecipes
        self.recipeNo = recipeNo
        self.speeduped = speeduped
        self.type = 'cookGraveWithBrains'
        self.x = x
        self.y = y


class GameCountedItem(GameType):
    type = 'countedItem'

    def __init__(self, count=None,  # @ReservedAssignment
                 finished=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (finished is None
                or isinstance(finished, bool))
        self.count = count
        self.finished = finished
        self.type = 'countedItem'


class GameDecoration(GameType):
    type = 'decoration'

    def __init__(self, placeTime=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (placeTime is None
                or isinstance(placeTime, unicode))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@D_UMBRELLA2_2'
        self.placeTime = placeTime
        self.type = 'decoration'
        self.x = x
        self.y = y


class GameDiggerGrave(GameType):
    type = 'diggerGrave'

    def __init__(self, started=None,  # @ReservedAssignment
                 gainDone=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainDone is None
                or isinstance(gainDone, long))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainDone = gainDone
        self.id = id
        self.item = '@SC_DIGGER_GRAVE'
        self.materials = materials
        self.started = started
        self.type = 'diggerGrave'
        self.x = x
        self.y = y


class GameDiggerGraveWithBrains(GameType):
    type = 'diggerGraveWithBrains'

    def __init__(self, gainTime=None,  # @ReservedAssignment
                 started=None,  # @ReservedAssignment
                 gainDone=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainDone is None
                or isinstance(gainDone, long))
        assert (gainTime is None
                or isinstance(gainTime, unicode))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainDone = gainDone
        self.gainTime = gainTime
        self.id = id
        self.item = '@SC_FISHER_GRAVE_BRAINER'
        self.materials = materials
        self.started = started
        self.type = 'diggerGraveWithBrains'
        self.x = x
        self.y = y


class GameEVT(GameType):
    type = 'EVT'

    def __init__(self, events=None):  # @ReservedAssignment
        assert (events is None
                or isinstance(events, list))
        self.events = events
        self.type = 'EVT'


class GameElvisTeamGrave(GameType):
    type = 'elvisTeamGrave'

    def __init__(self, started=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@SC_TEAM_GRAVE_WITH_BRAINS'
        self.started = started
        self.type = 'elvisTeamGrave'
        self.x = x
        self.y = y


class GameFruitTree(GameType):
    type = 'fruitTree'

    def __init__(self, fruitingCount=None,  # @ReservedAssignment
                 fertilized=None,  # @ReservedAssignment
                 jobFinishTime=None,  # @ReservedAssignment
                 jobStartTime=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (fertilized is None
                or isinstance(fertilized, bool))
        assert (fruitingCount is None
                or isinstance(fruitingCount, long))
        assert (id is None
                or isinstance(id, long))
        assert (jobFinishTime is None
                or isinstance(jobFinishTime, unicode))
        assert (jobStartTime is None
                or isinstance(jobStartTime, unicode))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.fertilized = fertilized
        self.fruitingCount = fruitingCount
        self.id = id
        self.item = '@FT_MANDARINE'
        self.jobFinishTime = jobFinishTime
        self.jobStartTime = jobStartTime
        self.type = 'fruitTree'
        self.x = x
        self.y = y


class GameGameMission(GameType):
    type = 'gameMission'

    def __init__(self, disabled=None,  # @ReservedAssignment
                 finished=None,  # @ReservedAssignment
                 tasks=None):  # @ReservedAssignment
        assert (disabled is None
                or isinstance(disabled, bool))
        assert (finished is None
                or isinstance(finished, bool))
        assert (tasks is None
                or isinstance(tasks, GameTasks))
        self.disabled = disabled
        self.finished = finished
        self.item = '@Q15_11'
        self.tasks = tasks
        self.type = 'gameMission'


class GameGuardGrave(GameType):
    type = 'guardGrave'

    def __init__(self, started=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@SC_GUARD_GRAVE'
        self.started = started
        self.type = 'guardGrave'
        self.x = x
        self.y = y


class GameHalloweenTower(GameType):
    type = 'halloweenTower'

    def __init__(self, users=None,  # @ReservedAssignment
                 level=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (level is None
                or isinstance(level, long))
        assert (users is None
                or isinstance(users, list))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_HALLOWEEN'
        self.level = level
        self.type = 'halloweenTower'
        self.users = users
        self.x = x
        self.y = y


class GameMetroEnter(GameType):
    type = 'metroEnter'

    def __init__(self, y=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@METRO_ENTER'
        self.type = 'metroEnter'
        self.x = x
        self.y = y


class GameMetroExit(GameType):
    type = 'metroExit'

    def __init__(self, y=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@METRO_EXIT'
        self.type = 'metroExit'
        self.x = x
        self.y = y


class GameMoveGameObjectToLocation(GameType):
    type = 'moveGameObjectToLocation'

    def __init__(self, finished=None):  # @ReservedAssignment
        assert (finished is None
                or isinstance(finished, bool))
        self.finished = finished
        self.type = 'moveGameObjectToLocation'


class GameNEW_YEAR(GameType):
    type = 'NEW_YEAR'

    def __init__(self, count=None,  # @ReservedAssignment
                 free=None,  # @ReservedAssignment
                 user=None,  # @ReservedAssignment
                 msg=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (free is None
                or isinstance(free, bool))
        assert (id is None
                or isinstance(id, long))
        assert (msg is None
                or isinstance(msg, unicode))
        assert (user is None
                or isinstance(user, unicode))
        self.count = count
        self.free = free
        self.id = id
        self.item = '@CR_11'
        self.msg = msg
        self.type = 'NEW_YEAR'
        self.user = user


class GameNewYearTree(GameType):
    type = 'newYearTree'

    def __init__(self, users=None,  # @ReservedAssignment
                 level=None,  # @ReservedAssignment
                 nextPlayTimes=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (level is None
                or isinstance(level, long))
        assert (nextPlayTimes is None
                or isinstance(nextPlayTimes, GameNextPlayTimes))
        assert (users is None
                or isinstance(users, list))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_SPRUCE_BIG'
        self.level = level
        self.nextPlayTimes = nextPlayTimes
        self.type = 'newYearTree'
        self.users = users
        self.x = x
        self.y = y


class GamePickup(GameType):
    type = 'pickup'

    def __init__(self, parentId=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (parentId is None
                or isinstance(parentId, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@SC_PICKUP_BOX_CAR'
        self.parentId = parentId
        self.type = 'pickup'
        self.x = x
        self.y = y


class GamePier(GameType):
    type = 'pier'

    def __init__(self, level=None,  # @ReservedAssignment
                 nextPlayTimes=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (level is None
                or isinstance(level, long))
        assert (nextPlayTimes is None
                or isinstance(nextPlayTimes, GameNextPlayTimes))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_PEAR2'
        self.level = level
        self.nextPlayTimes = nextPlayTimes
        self.type = 'pier'
        self.x = x
        self.y = y


class GamePlant(GameType):
    type = 'plant'

    def __init__(self, fertilized=None,  # @ReservedAssignment
                 jobFinishTime=None,  # @ReservedAssignment
                 jobStartTime=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (fertilized is None
                or isinstance(fertilized, bool))
        assert (id is None
                or isinstance(id, long))
        assert (jobFinishTime is None
                or isinstance(jobFinishTime, unicode))
        assert (jobStartTime is None
                or isinstance(jobStartTime, unicode))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.fertilized = fertilized
        self.id = id
        self.item = '@P_07'
        self.jobFinishTime = jobFinishTime
        self.jobStartTime = jobStartTime
        self.type = 'plant'
        self.x = x
        self.y = y


class GameSTART(GameType):
    type = 'START'

    def __init__(self, lang=None,  # @ReservedAssignment
                 info=None,  # @ReservedAssignment
                 ad=None,  # @ReservedAssignment
                 serverTime=None,  # @ReservedAssignment
                 clientTime=None):  # @ReservedAssignment
        assert (ad is None
                or isinstance(ad, unicode))
        assert (clientTime is None
                or isinstance(clientTime, long))
        assert (info is None
                or isinstance(info, GameInfo))
        assert (lang is None
                or isinstance(lang, unicode))
        assert (serverTime is None
                or isinstance(serverTime, long))
        self.ad = ad
        self.clientTime = clientTime
        self.info = info
        self.lang = lang
        self.serverTime = serverTime
        self.type = 'START'


class GameSlag(GameType):
    type = 'Slag'

    def __init__(self, y=None,  # @ReservedAssignment
                 id=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@SLAG'
        self.type = 'Slag'
        self.x = x
        self.y = y


class GameSocial(GameType):
    type = 'social'

    def __init__(self, disabled=None,  # @ReservedAssignment
                 finished=None,  # @ReservedAssignment
                 limitShow=None):  # @ReservedAssignment
        assert (disabled is None
                or isinstance(disabled, bool))
        assert (finished is None
                or isinstance(finished, bool))
        assert (limitShow is None
                or isinstance(limitShow, bool))
        self.disabled = disabled
        self.finished = finished
        self.item = '@MI_SOCIAL'
        self.limitShow = limitShow
        self.type = 'social'


class GameStayOnLocation(GameType):
    type = 'stayOnLocation'

    def __init__(self, finished=None):  # @ReservedAssignment
        assert (finished is None
                or isinstance(finished, bool))
        self.finished = finished
        self.type = 'stayOnLocation'


class GameStone(GameType):
    type = 'stone'

    def __init__(self, materialCount=None,  # @ReservedAssignment
                 gainStarted=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainStarted is None
                or isinstance(gainStarted, bool))
        assert (id is None
                or isinstance(id, long))
        assert (materialCount is None
                or isinstance(materialCount, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainStarted = gainStarted
        self.id = id
        self.item = '@SC_STONE23'
        self.materialCount = materialCount
        self.type = 'stone'
        self.x = x
        self.y = y

class GameStoneGraveDouble(GameType):
    type = 'stoneGraveDouble'

    def __init__(self, target=None,  # @ReservedAssignment
                 startCounter=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 doneCounter=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (doneCounter is None
                or isinstance(doneCounter, long))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, list))
        assert (startCounter is None
                or isinstance(startCounter, long))
        assert (target is None
                or isinstance(target, NoneType))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.doneCounter = doneCounter
        self.id = id
        self.item = '@SC_STONE_GRAVE2'
        self.materials = materials
        self.startCounter = startCounter
        self.target = target
        self.type = 'stoneGraveDouble'
        self.x = x
        self.y = y

class GameStoneGrave(GameType):
    type = 'stoneGrave'

    def __init__(self, target=None,  # @ReservedAssignment
                 startCounter=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 doneCounter=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (doneCounter is None
                or isinstance(doneCounter, long))
        assert (id is None
                or isinstance(id, long))
        assert (materials is None
                or isinstance(materials, list))
        assert (startCounter is None
                or isinstance(startCounter, long))
        assert (target is None
                or isinstance(target, NoneType))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.doneCounter = doneCounter
        self.id = id
        self.item = '@SC_STONE_GRAVE'
        self.materials = materials
        self.startCounter = startCounter
        self.target = target
        self.type = 'stoneGrave'
        self.x = x
        self.y = y


class GameTHANKSGIVING(GameType):
    type = 'THANKSGIVING'

    def __init__(self, count=None,  # @ReservedAssignment
                 free=None,  # @ReservedAssignment
                 user=None,  # @ReservedAssignment
                 msg=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (free is None
                or isinstance(free, bool))
        assert (id is None
                or isinstance(id, long))
        assert (msg is None
                or isinstance(msg, unicode))
        assert (user is None
                or isinstance(user, unicode))
        self.count = count
        self.free = free
        self.id = id
        self.item = '@CR_113'
        self.msg = msg
        self.type = 'THANKSGIVING'
        self.user = user


class GameTIME(GameType):
    type = 'TIME'

    def __init__(self, key=None):  # @ReservedAssignment
        self.type = 'TIME'
        self.key = key


class GameThanksgivingTable(GameType):
    type = 'thanksgivingTable'

    def __init__(self, users=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 usedPlatesCount=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (id is None
                or isinstance(id, long))
        assert (usedPlatesCount is None
                or isinstance(usedPlatesCount, long))
        assert (users is None
                or isinstance(users, list))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.id = id
        self.item = '@B_BULB_TABLE4_1'
        self.type = 'thanksgivingTable'
        self.usedPlatesCount = usedPlatesCount
        self.users = users
        self.x = x
        self.y = y

class GameCookSpeed(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'speedup'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'

class GameCookItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'cook'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'

class GameCookStart(GameAction):
    type = 'item'

    def __init__(self, objId=None):  # @ReservedAssignment
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'start'
        self.objId = objId
        self.type = 'item'

class GameCookStop(GameAction): 
    #{"objId":803,"action":"stop","type":"item"}
    type = 'item'
    
    def __init__(self, objId=None):  # @ReservedAssignment
        assert (objId is None
                or isinstance(objId, long))
        self.objId = objId
        self.type = 'item'
        self.action = 'stop'


class GameBuyItem(GameAction):
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.action = 'buy'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'
        self.x = x
        self.y = y
        
class GameUseStorageItem(GameAction):
    type = 'item'
    def __init__(self,  # @ReservedAssignment
                 itemId=None,
                 y=None,  # @ReservedAssignment
                 x=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        # assert (objId is None
                # or isinstance(objId, long))
        assert (x is None or isinstance(x, long))
        assert (y is None  or isinstance(y, long))
        self.action = 'useStorageItem'
        self.itemId = itemId
        # self.objId = objId
        self.type = 'item'
        self.x = x
        self.y = y
        
class GameSellItem(GameAction):
    type = 'item'

    def __init__(self, 
                count=None,
                itemId=None ): #,  # @ReservedAssignment
        assert (count is None
                or isinstance(count, long))
        assert (itemId is None
                or isinstance(itemId, unicode))
        self.count = count
        self.action = 'sell'
        self.itemId = itemId
        self.type = 'item'

class GameCookSpeedItem(GameAction):
    type = 'item'
    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'speedup'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'

class GameCraftItem(GameAction): # "events":[{"objId":-4244,      "action":"craft",       "type":"item",          "itemId":"1"}],
    type = 'item'

    def __init__(self, itemId=None,  # @ReservedAssignment
                 objId=None):   # @ReservedAssignment
        assert (itemId is None
                or isinstance(itemId, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'craft'
        self.itemId = itemId
        self.objId = objId
        self.type = 'item'

# "events":[{"gift":{"msg":"","count":1,"user":"176312587","item":"@CAKE_RABBIT"},"action":"sendGift","id":42,"type":"gift"}],"user":"13504693","id":1368083522531,"type":"EVT"}
# "events":[{"gift":{"msg":"","count":1,"user":"114688858","item":"@CAKE_RABBIT"},"action":"sendGift","id":41,"type":"gift"}],"user":"13504693","id":1368083522519,"type":"EVT"}
# "events":[{"gift":{"item":"@CR_53","msg":"","count":1,"user":"176312587"},"action":"sendGift","id":55,"type":"gift"}],"type":"EVT"}
#{"gift":{"item":"@CR_53","msg":"","count":1,"user":"176312587"},"action":"sendGift","id":55,"type":"gift"}
# gift msg="", count=None, user=none,
class GameSendGift(GameAction):
    type = 'gift'
    def __init__(self, id=None, gift=None):  # @ReservedAssignment
        assert (gift is None
                or isinstance(gift, dict))
                #or isinstance(gift, GameGift))
        self.action = 'sendGift'
        self.gift = gift
        self.type = 'gift'

# {"itemId":"RED_TREE_FERTILIZER","action":"fertilize","objId":9072,"type":"item"}

class GameFertilizeTree(GameAction):
    type = 'item'
    
    def __init__(self, itemId=None, objId=None):  # @ReservedAssignment   , ItemId=None
        assert (objId is None
                or isinstance(objId, long))
        assert (itemId is None
                or isinstance(itemId, unicode))
        self.itemId = itemId
        self.action = 'fertilize'
        self.objId = objId
        self.type = 'item'


class DailyBonus(GameAction):
    type = 'dailyBonus'

    def __init__(self):

        self.type = 'dailyBonus'
        self.action = 'play'



class GameFertilizePlant(GameAction):
    type = 'plant'

    def __init__(self, jobFinishTime=None,  # @ReservedAssignment
                 jobStartTime=None,  # @ReservedAssignment
                 objId=None):  # @ReservedAssignment
        assert (jobFinishTime is None
                or isinstance(jobFinishTime, unicode))
        assert (jobStartTime is None
                or isinstance(jobStartTime, unicode))
        assert (objId is None
                or isinstance(objId, long))
        self.action = 'fertilize'
        self.jobFinishTime = jobFinishTime
        self.jobStartTime = jobStartTime
        self.objId = objId
        self.type = 'plant'


class GameTraderGrave(GameType):
    type = 'traderGrave'

    def __init__(self, started=None,  # @ReservedAssignment
                 gainDone=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainDone is None
                or isinstance(gainDone, long))
        assert (id is None
                or isinstance(id, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainDone = gainDone
        self.id = id
        self.item = '@SC_TRADER_GRAVE_COINS'
        self.started = started
        self.type = 'traderGrave'
        self.x = x
        self.y = y


class GameTraderGraveWithBrains(GameType):
    type = 'traderGraveWithBrains'

    def __init__(self, gainTime=None,  # @ReservedAssignment
                 started=None,  # @ReservedAssignment
                 gainDone=None,  # @ReservedAssignment
                 materials=None,  # @ReservedAssignment
                 y=None,  # @ReservedAssignment
                 x=None,  # @ReservedAssignment
                 id=None):  # @ReservedAssignment
        assert (gainDone is None
                or isinstance(gainDone, long))
        assert (id is None
                or isinstance(id, long))
        assert (started is None
                or isinstance(started, bool))
        assert (x is None
                or isinstance(x, long))
        assert (y is None
                or isinstance(y, long))
        self.gainDone = gainDone
        self.gainTime = gainTime
        self.id = id
        self.item = '@SC_TRADER_GRAVE_WITH_BRAINS'
        self.started = started
        self.type = 'traderGraveWithBrains'
        self.x = x
        self.y = y


class GamePirateCapture (GameAction):
    type = 'pirateCaptureObject'


if __name__ == '__main__':
    pass
