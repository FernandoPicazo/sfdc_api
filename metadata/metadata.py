# Basic library for interfacing with the Salesforce Metadata API
# Currently only implements the necessary calls to retrieve metadata
# If further calls are made functionality should probably be split up under a few child repos


class Metadata:
    _CONNECTION = None

    def __init__(self, connection):
        self._CONNECTION = connection

    def read(self, metadata_type, names):
        headers = {'content-type': 'text/xml', 'SOAPAction': '""'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:met="http://soap.sforce.com/2006/04/metadata">\
            <soapenv:Header>
            <met:CallOptions>
            </met:CallOptions>
            <met:SessionHeader>
            <met:sessionId>""" + self._CONNECTION.login_response['session_id']  + """</met:sessionId>
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
        endpoint = self._CONNECTION.login_response['metadata_server_url']
        return self._CONNECTION.send_http_request(endpoint, 'POST', headers, body=body.encode('utf-8'))

    def retrieve(self, package):
        print('TODO')