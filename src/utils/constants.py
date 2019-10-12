import enum


class AuthenticationMode(enum.IntEnum):
    unauthenticated = -1
    username_password_rest_flow = 0
    web_server_rest_flow = 1
    user_agent_rest_flow = 2
    username_password_soap_flow = 3

# Dictionary of default headers used in order to better streamline creation of new requests to the salesforce api
HEADERS = {
    "oauth_login_headers": {"Content-Type": "application/x-www-form-urlencoded"},
    "soap_login_headers": {"Content-Type": "text/xml", "SOAPAction": '""' },
    "rest_authorized_headers": {
        "Authorization": None,
        "Content-Type": "application/json",
        "charset": "UTF-8"
    },
    "soap_authorized_headers": {} #TODO: get the generic structure for this
}
