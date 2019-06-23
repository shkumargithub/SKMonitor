import requests
import logging as logger
from SKLibPY.WebLogic.WLSObject import WLSObject
from SKLibPY.WebLogic.WLSExceptions import *

DEFAULT_TIMEOUT = 60
__version__ = '0.1.2'


class WLS(object):
    """
    Represents a WLS REST server
    :param string host: protocol://hostname:port of the server.
    :param string username: Username used to authenticate against the server
    :param string password: Password used to authenticate against the server
    :param string version: Version of the rest interface to use. Defaults to "latest"
    :param bool verify_ssl: Whether to verify certificates on SSL connections.
    """

    def __init__(self, host, username, password, version='latest', verify=True,
                 timeout=DEFAULT_TIMEOUT):
        self.session = requests.Session()
        self.session.verify = verify
        self.session.auth = (username, password)
        user_agent = 'wls-rest-python {} ({})'.format(
            __version__, self.session.headers['User-Agent']
        )
        self.session.headers.update(
            {'Accept': 'application/json', 'User-Agent': user_agent, 'X-Requested-By': user_agent}
        )
        self.timeout = timeout
        self.base_url = '{}/management/weblogic/{}'.format(host, version)
        collection = self.get(self.base_url)
        self.version = collection['version']
        self.isLatest = collection['isLatest']
        self.lifecycle = collection['lifecycle']
        for link in collection['links']:
            link_obj = WLSObject(link['rel'], link['href'], self)
            setattr(self, link['rel'], link_obj)

    def get(self, url, **kwargs):
        """
        Does a GET request to the specified URL.
        Returns the decoded JSON.
        """
        response = self.session.get(url, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def post(self, url, prefer_async=False, **kwargs):
        """
        Does a POST request to the specified URL.
        If the response is a job or an collection, it will return an
        WLSObject. Otherwise it will return the decoded JSON
        """
        headers = {'Prefer': 'respond-async'} if prefer_async else None
        response = self.session.post(url, headers=headers, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def delete(self, url, prefer_async=False, **kwargs):
        """
        Does a DELETE request to the specified URL.
        If the response is a job or an collection, it will return an
        WLSObject. Otherwise it will return the decoded JSON
        """
        headers = {'Prefer': 'respond-async'} if prefer_async else None
        response = self.session.delete(url, headers=headers, timeout=self.timeout, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        logger.debug(
            'Sent %s request to %s, with headers:\n%s\n\nand body:\n%s',
            response.request.method,
            response.request.url,
            '\n'.join(["{0}: {1}".format(k, v) for k, v in response.request.headers.items()]),
            response.request.body,
        )
        logger.debug(
            'Recieved response:\nHTTP %s\n%s\n\n%s',
            response.status_code,
            '\n'.join(["{0}: {1}".format(k, v) for k, v in response.headers.items()]),
            response.content.decode(),
        )

        if not response.ok:
            self._handle_error(response)

        # GET is used by the WLSObject to retrieve the collection
        # so it must return only the decoded JSON, not an WLSobject
        if response.request.method == 'GET':
            return response.json()

        response_json = response.json()
        if not response_json:
            return None

        try:
            link = next((x['href'] for x in response_json['links'] if x['rel'] in ('self', 'job')))
            name = response_json['name']
        except (KeyError, StopIteration):
            # Not a job, and not a collection.
            # Don't know what it is, so just return the decoded json
            return response_json

        return WLSObject(name, link, self)

    @staticmethod
    def _handle_error(response):
        if response.status_code == 400:
            raise BadRequestException(response.json()['detail'])

        if response.status_code == 401:
            # does not return json
            raise UnauthorizedException()

        if response.status_code == 403:
            raise ForbiddenException(response.json()['detail'])

        if response.status_code == 404:
            raise NotFoundException(response.json()['detail'])

        if response.status_code == 405:
            raise MethodNotAllowedException(response.json()['detail'])

        if response.status_code == 406:
            raise NotAcceptableException(response.json()['detail'])

        if response.status_code == 500:
            # may not return json...
            try:
                raise ServerErrorException(response.json()['detail'])
            except ValueError:
                pass
            raise ServerErrorException(response.text)

        if response.status_code == 503:
            raise ServiceUnavailableException(response.json()['detail'])

        print(response)
        raise WLSException(
            'An unknown error occured. Got status code: {}'.format(response.status_code)
        )

