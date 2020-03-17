from json import dumps
"""
#Class: SObject
#   Purpose: This class serves as an abstraction of the SObject model within the Salesforce Tooling API
#TODO: Error handling and presentation
"""
class SObject:
    _CONNECTION = None
   
    """
    #Function: __init__
    #   Purpose: Constructor for SObject, passed in a Connection object reference, for the purpose of sending http requests
    """
    def __init__(self, conn):
        self._CONNECTION = conn
        self.base_endpoint = self._CONNECTION.CONNECTION_DETAILS['instance_url'] + 'services/data/tooling/v' + \
                             str(self._CONNECTION.VERSION) + '/sobjects/'
    
    """
    #Function: list_sobjects
    #   Purpose: Lists all available object under the SObject domain in the tooling API
    """
    def global_describe(self):
        headers = self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers']
        return self._CONNECTION.send_http_request(self.base_endpoint, "GET", headers)

    """
    #Function: list_sobjects
    #   Purpose: Lists all available object under the SObject domain in the tooling API
    """

    def list_sobjects(self):
        return self._CONNECTION.send_http_request(self.base_endpoint, 'GET',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'])

    """
    #Function: create
    #   Purpose: Creates an sobject with the given information, receives json as the body of the http request
    #   Receives: name- name of the sobject type, body - a dictionary of all fields required to create the new object
    """

    def create(self, name, body, *opts):
        url_opts = ''
        if opts:
            url_opts = '/'.join(opts)
        endpoint = self.base_endpoint + name + '/' + url_opts
        return self._CONNECTION.send_http_request(endpoint, 'POST',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'],
                                                  dumps(body).encode('utf8'))

    """
    #Function: describe
    #   Purpose: describes a specific object in the TOOLING API
    #   Receives:   name - name of subject object to study, 
    #                [detail]- optional flag, used to describe all fields associated with an object
    """

    def describe(self, name, detail=False):
        endpoint = self.base_endpoint + name
        if detail:
            endpoint += '/describe/'
        else:
            endpoint += '/'
        return self._CONNECTION.send_http_request(endpoint, 'GET',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'])

    """
    #Function: get_by_id
    #   Purpose: gets a specific instance of an object and describes the associated fields
    """

    def get_by_id(self, name, id, *opts):
        url_opts = ''
        if opts:
            url_opts = '/'.join(opts)
        endpoint = self.base_endpoint + name + '/' + id + '/' + url_opts
        return self._CONNECTION.send_http_request(endpoint, 'GET',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'])

    """
    #Function: delete
    #   Purpose: deletes a specific instance of an object
    """

    def delete(self, name, id, *opts):
        url_opts = ''
        if opts:
            url_opts = '/'.join(opts)
        endpoint = self.base_endpoint + name + '/' + id + '/' + url_opts
        return self._CONNECTION.send_http_request(endpoint, 'DELETE',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'])

    """
    #Function: update
    #   Purpose: used to update the fields associated with a specific object
    """

    def update(self, name, id, body, *opts):
        url_opts = ''
        if opts:
            url_opts = '/'.join(opts)
        endpoint = self.base_endpoint + name + '/' + id + '/' + url_opts
        return self._CONNECTION.send_http_request(endpoint, 'PATCH',
                                                  self._CONNECTION.HTTPS_HEADERS['rest_authorized_headers'],
                                                  dumps(body).encode('utf8'))