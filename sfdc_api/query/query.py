from sfdc_api.utils import Connection
from urllib.parse import quote


class QueryResult(dict):
    def __init__(self, conn, *args, **kw):
        self.__CONNECTION = conn
        super(QueryResult, self).__init__(*args, **kw)

    def query_more(self):
        if 'nextRecordsUrl' in self.keys() and self.get('nextRecordsUrl') != '':
            endpoint = self.__CONNECTION.CONNECTION_DETAILS["instance_url"] + self.get('nextRecordsUrl')
            return QueryResult(self.__CONNECTION, **self.__CONNECTION.send_http_request(endpoint, "GET",
                                                                                        self.__CONNECTION.HTTPS_HEADERS[
                                                                                            'rest_authorized_headers']))
        return None

    def query_all(self):
        while True:
            if 'nextRecordsUrl' in self.keys() and self.get('nextRecordsUrl') != '':
                ret = self.query_more()
                if ret is None or self['done']:
                    break
                self['totalSize'] = ret['totalSize']
                self['done'] = ret['done']
                self['records'].extend(ret['records'])
                if 'nextRecordsUrl' in ret.keys():
                    self['nextRecordsUrl'] = ret['nextRecordsUrl']
                else:
                    del self['nextRecordsUrl']
            else:
                break
        return self


class Query:
    _CONNECTION = None

    def __init__(self, conn: Connection, parent_service_extension: str = ''):
        self._CONNECTION = conn
        self.service_endpoint = self._CONNECTION.CONNECTION_DETAILS["instance_url"] + '/services/data/v' + \
                   str(self._CONNECTION.VERSION) + '/' + parent_service_extension + '/query/'

    def query(self, query='', explain=False, query_identifier='') -> QueryResult:
        endpoint = self.service_endpoint
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
        return QueryResult(self._CONNECTION, **self._CONNECTION.send_http_request(endpoint, "GET",
                                                                                  self._CONNECTION.HTTPS_HEADERS[
                                                                                      'rest_authorized_headers']))
