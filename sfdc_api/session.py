# This class serves as an intermediary between the Connection module and every other API module
# Basically just serves a driver for neater API interactions
# This class can further see improvement by providing handling for out of order execution
# Links objects together 
from .utils import Connection
from .tooling import Tooling
from .query import Query
from .metadata import Metadata
from .sobjects import Sobjects
from .wsdl import WSDL


class Session:
    # doesn't store much more than the actual classes, should probably store some more information
    connection = None
    tooling = None
    query = None
    metadata = None
    sobjects = None
    wsdl = None

    # def __init__(self, org_username, org_password, client_id, client_key, org_url):
    def __init__(self, args: dict):
        # initialize connection objects only
        self.connection = Connection(args)

    def login(self):
        login_response = self.connection.login()
        self.tooling = Tooling(self.connection)
        self.query = Query(self.connection)
        self.metadata = Metadata(self.connection)
        self.sobjects = Sobjects(self.connection)
        self.wsdl = WSDL(self.connection)
        return login_response

    def logout(self):
        self.connection.logout()
