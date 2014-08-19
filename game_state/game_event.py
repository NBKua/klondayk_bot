from types import NoneType
from game_state.mixins import CommonEqualityMixin


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def dict2obj(d, name=None):
        if isinstance(d, list):  # handle list
            if name:
                name = name.rstrip('s')
            d = [dict2obj(x, name) for x in d]
        if not isinstance(d, dict):  # handle simple types
            if not isinstance(d, bool):
                if isinstance(d, int):   # use only long types
                    d = long(d)          # (causes errors on android)
            return d

        class_name = ''
        # d is dict, handle complex type
        if 'action' in d and is_ascii(d['action']):
            class_name = d['action']
        if 'type' in d and not class_name.upper().endswith(
                                                    (d['type'].upper())
                                                    ):
            class_name += d['type'][0].upper() + d['type'][1:]
        elif 'cmd' in d:
            class_name = d['cmd'] + 'Command'
        elif name is not None:
            if name == 'event':
                class_name += "Event"
            elif name == 'mission':
                class_name += "Mission"
            else:
                class_name += name
        else:
            class_name = 'UnknownObject'
        class_name = 'Game' + class_name[0].upper() + class_name[1:]
        if 'action' in d:
            base_class_name = 'GameAction'
            base_class = type(base_class_name, (object,), {})
        elif 'type' in d:
            base_class_name = 'GameType'
            base_class = type(base_class_name, (object,), {})
        elif 'item' in d:
            base_class_name = 'GameItem'
            base_class = type(base_class_name, (object,), {})
        else:
            base_class = CommonEqualityMixin
        constructor = type(str(class_name), (base_class,), {})
        o = constructor()
        for k in d:
            o.__dict__[k] = dict2obj(d[k], k)
        return o


def obj2dict(obj):
    # handle list
    if isinstance(obj, list):
        d = [obj2dict(x) for x in obj]
    # handle simple types
    elif (isinstance(obj, str) or
          isinstance(obj, bool) or
          isinstance(obj, int) or
          isinstance(obj, long) or
          isinstance(obj, float) or
          isinstance(obj, unicode) or
          isinstance(obj, NoneType)):
        d = obj
    else:
        # handle dict
        d = {}
        if not isinstance(obj, dict):
            obj = obj.__dict__
        for key in obj:
            new_dict = obj2dict(obj[key])
            if new_dict is not None:  # skip None types
                d[key] = new_dict
    return d


class GameAction(object):
    def __init__(self, action):
        self.action = action


class GiftEvent(GameAction):

    def __init__(self, action, gift):
        super(GiftEvent, self).__init__(action)
        self.gift = gift
        self.type = 'gift'


class Gift(object):

    def __init__(self, gift_id):
        self.id = gift_id


class ApplyGiftEvent(GiftEvent):

    def __init__(self, gift):
        super(ApplyGiftEvent, self).__init__('applyGift', gift)
