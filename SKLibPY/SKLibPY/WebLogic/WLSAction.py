class WLSAction(object):
    """
    An action from a collection.
    Identified by a link with rel=action.
    """

    def __init__(self, name, url, wls):
        self._url = url
        self._name = name
        self._wls = wls

    def __call__(self, prefer_async=False, **kwargs):
        return self._wls.post(self._url, prefer_async,
                              json=kwargs if kwargs else {})