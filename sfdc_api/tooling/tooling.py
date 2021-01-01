import sfdc_api
from sfdc_api.sobjects import SObject
from .runtests import RunTests
from ..query.query import Query
from urllib.parse import quote


class Tooling:
    _CONNECTION = None
    sobjects = None
    runtests = None

    def __init__(self, conn):
        self._CONNECTION = conn
        self.sobjects = SObject(self._CONNECTION)
        self.runtests = RunTests(self._CONNECTION)
        self._query = Query(self._CONNECTION, 'tooling')

    def completions(self):
        print("Hello from the completions function")

    def execute_anonymous(self):
        print("Hello from the executeAnonymous function")

    def search(self):
        print("Hello from the search function")

    def query(self, query='', explain=False, query_identifier=''):
        return self._query.query(query, explain, query_identifier)