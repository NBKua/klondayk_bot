class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (other.__class__.__name__ == self.__class__.__name__
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__class__.__name__ + ': ' + str(self)
