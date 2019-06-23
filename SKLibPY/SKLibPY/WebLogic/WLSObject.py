from SKLibPY.WebLogic.WLSAction import WLSAction
from SKLibPY.WebLogic.WLSItems import WLSItems


class WLSObject(object):
    """
    Represents all the different WLS objects.
    The attributes will differ based on the
    collection used to instantiate it
    """

    def __init__(self, name, url, wls):
        self._name = name
        self._url = url
        self._wls = wls

    def __dir__(self):
        attrs = []
        collection = self._wls.get(self._url)
        for key in collection:
            item = collection[key]
            if key == 'links':
                for link in item:
                    if link['rel'] == 'action':
                        name = link['title']
                    else:
                        name = link['rel']
                    attrs.append(name)
            elif key == 'items':
                for itm in item:
                    attrs.append(itm['name'])
            else:
                attrs.append(key)
        return attrs

    def __getattr__(self, attr):
        """
        Retrieves the properties dynamically from the collection
        We store actions and links for re-use, since they are expected not to change
        """
        collection = self._wls.get(self._url)
        for key in collection:
            item = collection[key]
            if key == 'links':
                for link in item:
                    if link['rel'] == 'action':
                        name = link['title']
                        if name == attr:
                            obj = WLSAction(name, link['href'], self._wls)
                            setattr(self, name, obj)
                            return obj

                    else:
                        name = link['rel']
                        if name == attr:
                            obj = WLSObject(name, link['href'], self._wls)
                            setattr(self, name, obj)
                            return obj

            elif key == 'items':
                for itm in item:
                    if itm['name'] == attr:
                        self_link = next((x['href'] for x in itm['links'] if x['rel'] == 'self'))
                        return WLSObject(itm['name'], self_link, self._wls)

            else:
                if key == attr:
                    return item

        raise AttributeError('\'{}\' object has no attribute \'{}\''.format(self._name, attr))

    def __getitem__(self, key):
        # this is here for items with weird names
        # e.g. webapps with version number (myWebapp#1.2.3)
        try:
            return self.__getattr__(key)
        except AttributeError:
            pass
        raise KeyError(key)

    def __iter__(self):
        collection = self._wls.get(self._url)
        is_iterable = False
        iter_items = []
        for key in collection:
            item = collection[key]
            if key == 'items':
                is_iterable = True
                for itm in item:
                    self_link = next((x['href'] for x in itm['links'] if x['rel'] == 'self'))
                    iter_items.append(WLSObject(itm['name'], self_link, self._wls))
        if is_iterable:
            return WLSItems(iter_items)

        raise TypeError('\'{}\' object is not iterable'.format(self._name))

    def delete(self, prefer_async=False, **kwargs):
        """
        Deletes the resource. Will result in an DELETE request to the self url
        The kwargs are sendt through to requests
        """
        return self._wls.delete(self._url, prefer_async, **kwargs)

    def create(self, prefer_async=False, **kwargs):
        """
        Creates a resource. Will result in an POST request to the self url
        The kwargs are sendt through to requests
        """
        return self._wls.post(self._url, prefer_async, **kwargs)

    def update(self, prefer_async=False, **kwargs):
        """
        Updates an property of the resource.
        The kwargs will be sent as json
        """
        return self._wls.post(self._url, prefer_async, json=kwargs)
