
from types import NoneType
from collections import OrderedDict
from sets import Set
import json
from game_state.game_event import dict2obj, obj2dict


class klass(object):

    def __init__(self, name, bases=[], attrs={}):
        self.name = name
        self.bases = bases
        self.attrs = attrs

    def __str__(self):
        string = 'class %s(%s):\n' % (self.name, ', '.join(self.bases))
        if self.attrs == {}:
            string += '    pass\n'
        else:
            if 'type' in self.attrs:
                string += "    type = '" + self.attrs['type'] + "'\n\n"
            is_reserved = len(Set(['list', 'id', 'type']).intersection(
                self.attrs.keys())) > 0
            if is_reserved:
                suppress_reserved = '  # @ReservedAssignment'
            else:
                suppress_reserved = ''
            string_join = ',%s\n                 ' % suppress_reserved
            attrs = filter(lambda x: (type(self.attrs[x]) == type),
                                      self.attrs.keys())
            attrs = [attr + '=None' for attr in attrs]
            string += ('    def __init__(self, %s):%s\n' %
                       (string_join.join(attrs),
                        suppress_reserved)
                       )
            for attr_name, attr_value in sorted(self.attrs.iteritems()):
                if type(attr_value) == type:
                    string += ('        assert (%s is None\n'
                               '                or isinstance(%s, %s))\n' %
                               (attr_name, attr_name, attr_value.__name__)
                              )
            for attr_name, attr_value in sorted(self.attrs.iteritems()):
                if type(attr_value) == type:
                    string += '        self.%s = %s\n' % (attr_name, attr_name)
                else:
                    string += '        self.%s = \'%s\'\n' % (attr_name,
                                                              attr_value)
        string += '\n\n'
        return string


def generate_klasses(obj):
    klasses = OrderedDict()
    # handle simple types
    if(isinstance(obj, str) or
       isinstance(obj, unicode) or
       isinstance(obj, int) or
       isinstance(obj, long) or
       isinstance(obj, NoneType)):
        pass
    # handle list
    elif isinstance(obj, list):
        for x in obj:
            klasses.update(generate_klasses(x))
    # handle dict
    elif isinstance(obj, dict):
        for key in obj:
            klasses.update(generate_klasses(obj[key]))
    else:
        class_name = type(obj).__name__
        class_bases = [base.__name__ for base in type(obj).__bases__]
        instance_attributes = {}
        for attr_name, attr_value in obj.__dict__.iteritems():
            attr_type = type(attr_value)
            if attr_name in ['action', 'type', 'item', 'cmd']:
                instance_attributes[attr_name] = attr_value
            else:
                instance_attributes[attr_name] = attr_type
        for key in obj.__dict__:
            klasses.update(generate_klasses(obj.__dict__[key]))
        for base in class_bases:
            if base != 'CommonEqualityMixin':
                klasses[base] = klass(base, ['CommonEqualityMixin'], {})
        klasses[class_name] = klass(class_name, class_bases,
                                    instance_attributes)
    return klasses


def generate_classes(obj):
    common_class = '''from mixins import CommonEqualityMixin
from types import NoneType


'''
    classes = generate_klasses(obj)
    string = common_class + generate_class(classes.keys(), classes)
    return string


def generate_class(class_names, classes):
    string = ''
    for klass_ in print_order(class_names, classes):
        string += str(classes[klass_])
    return string


def print_order(class_names, classes, printed=[]):
    ordered_class_names = []
    postponed_classes = []
    for klass_ in sorted(class_names):
        if(len(classes[klass_].bases) == 1 and
                klass_ not in printed and
                (classes[klass_].bases[0] == 'CommonEqualityMixin' or
                classes[klass_].bases[0] == 'object') or
                classes[klass_].bases[0] in printed):
            ordered_class_names += [klass_]
            printed += [klass_]
        else:
            postponed_classes += [klass_]
    if postponed_classes != []:
        ordered_class_names += print_order(postponed_classes, classes, printed)
    return ordered_class_names


if __name__ == '__main__':
    with open('game.json') as fp:
        start_response = json.load(fp)
    start_response_object = dict2obj(start_response)
    state_dict = obj2dict(start_response_object)
    #assert start_response == state_dict
    print generate_classes(start_response_object),
    print "if __name__ == '__main__':\n    pass"
