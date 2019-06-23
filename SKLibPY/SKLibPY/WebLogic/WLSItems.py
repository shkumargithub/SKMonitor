class WLSItems(object):
    """
    Items from an object.
    Used as an iterator
    """

    def __init__(self, items):
        self.items = items
        self.counter = 0

    def __next__(self):
        try:
            item = self.items[self.counter]
        except IndexError:
            raise StopIteration

        self.counter += 1
        return item

    def next(self):
        # python 2
        return self.__next__()