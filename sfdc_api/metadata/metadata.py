from ..utils import soap_body_builder
from urllib import parse


# Basic library for interfacing with the Salesforce Metadata API
# Currently only implements the necessary calls to retrieve metadata
# If further calls are made functionality should probably be split up under a few child repos


class Metadata:
    _CONNECTION = None

    def __init__(self, connection):
        self._CONNECTION = connection
        self._ENDPOINT = self._CONNECTION.CONNECTION_DETAILS['metadata_server_url']

    def read(self, metadata_type, names):
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">\
            <soapenv:Header>
            <met:CallOptions>
            </met:CallOptions>
            <met:SessionHeader>
            <met:sessionId>""" + self._CONNECTION.CONNECTION_DETAILS['session_id'] + """</met:sessionId>
            </met:SessionHeader>
            </soapenv:Header>
            <soapenv:Body>
            <met:readMetadata>
            <met:type>""" + metadata_type + """</met:type>
            <!--Zero or more repetitions:-->
            <met:fullNames>""" + names + """</met:fullNames>
            </met:readMetadata>
            </soapednv:Body>
            </soapenv:Envelope>"""
        endpoint = self._CONNECTION.CONNECTION_DETAILS['metadata_server_url']
        return self._CONNECTION.send_http_request(endpoint, 'POST', headers, body=body.encode('utf-8'))

    ###
    # Three possible ways to make a request for this endpoint LN:13710
    # - List of package names
    # - A list of specific files
    # - Unpackaged a package xml representations
    # Options:
    # - Single package: boolean dictating whether a single package will be created
    #
    # ####
    def retrieve(self, body):
        endpoint = self._CONNECTION.CONNECTION_DETAILS['metadata_server_url']
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        soap_body = soap_body_builder(self._CONNECTION.CONNECTION_DETAILS['session_id'], body)
        return self._CONNECTION.send_http_request(endpoint, 'POST', headers, body=soap_body.encode('utf-8'))

    # TODO: add the
    def check_retrieve_status(self, retrieve_id):
        endpoint = self._CONNECTION.CONNECTION_DETAILS['metadata_server_url']
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        body = ''.join([
            '<met:checkRetrieveStatus>',
            '<met:asyncProcessId>',
            retrieve_id,
            '</met:asyncProcessId>',
            '<includeZip type="xsd:boolean">true</includeZip>',
            '</met:checkRetrieveStatus>'
        ])
        soap_body = soap_body_builder(self._CONNECTION.CONNECTION_DETAILS['session_id'], body)
        return self._CONNECTION.send_http_request(endpoint, 'POST', headers, body=soap_body.encode('utf-8'))

    # TODO: add full support for multiple queries
    def list_metadata(self, meta_type, folder_name=''):
        endpoint = self._CONNECTION.CONNECTION_DETAILS['metadata_server_url']
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        retrieve_query_template = ''.join([
            '<folder>{}</folder>',
            '<type>{}</type>',
        ])
        list_metadata_request_template = ''.join([
            '<met:listMetadata>',
            '<met:queries>{}</met:queries>'
            '<met:asOfVersion>45.0</met:asOfVersion>',
            '</met:listMetadata>',
        ])
        retrieve_query = retrieve_query_template.format(folder_name, meta_type)
        list_metadata_request = list_metadata_request_template.format(retrieve_query)
        soap_body = soap_body_builder(self._CONNECTION.CONNECTION_DETAILS['session_id'], list_metadata_request)
        return self._CONNECTION.send_http_request(endpoint, 'POST', headers, body=soap_body.encode('utf-8'))

    def describe_metadata(self):
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        describe_metadata_template = ''.join([
            '<met:describeMetadata>',
            '<met:asOfVersion>45.0</met:asOfVersion>'
            '</met:describeMetadata>'
        ])
        soap_body = soap_body_builder(self._CONNECTION.CONNECTION_DETAILS['session_id'], describe_metadata_template)
        return self._CONNECTION.send_http_request(self._ENDPOINT, 'POST', headers, body= soap_body.encode('utf-8'))