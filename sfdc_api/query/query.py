from sfdc_api.utils import Connection
from urllib.parse import urlencode, quote


class Query:
    _CONNECTION = None

    def __init__(self, conn):
        self._CONNECTION = conn

    def query(self, query='', explain=False, query_identifier=''):
        endpoint = self._CONNECTION.CONNECTION_DETAILS["instance_url"] + '/services/data/v' + \
                       str(self._CONNECTION.VERSION) + '/query/'
        if query and not explain and not query_identifier:
            endpoint += '?q=' + quote(query)
        elif query and explain and not query_identifier:
            endpoint += '?explain=' + quote(query)
        elif not query and explain and query_identifier:
            endpoint += '?explain=' + quote(query_identifier)
        elif not query and not explain and query_identifier:
            endpoint += quote(query_identifier)
        else:
            raise ValueError('Incorrect parameter configuration')
        return self._CONNECTION.send_http_request(endpoint, "GET", self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'])
