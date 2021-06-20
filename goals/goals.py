#################
##### Goals #####
#################

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests as requests

import json
import secrets

class Goals:

    ##### Initializer #####
    def __init__(self):
        wifi.radio.connect(secrets.secrets['ssid'], secrets.secrets['password'])

        pool = socketpool.SocketPool(wifi.radio)
        self._https = requests.Session(pool, ssl.create_default_context())

        try:
            token = self._get_token()
        except (ValueError, RuntimeError) as e:
            print("Some error occured, retrying later -", e)
        
        headers = {'Authorization': 'Bearer ' + token}

        url = 'https://graph.microsoft.com/v1.0/me/onenote/pages'

        response = self._https.get(url, headers=headers)
        print(response.status_code)

        json_resp = response.json()
        print(json_resp)


    # Fetch access token
    def _get_token(self):
        data = {'grant_type': 'client_credentials',
                # 'grant_type': 'password',
                # 'username':'xxxx',
                # 'password':'xxxx',
                'client_id': secrets.azure['app_id'],
                'client_secret': secrets.azure['client_secret'],
                'scope': 'https://graph.microsoft.com/.default',
                'resource': 'https://graph.microsoft.com/'
                }
        url = 'https://login.microsoftonline.com/{}/oauth2/token'\
              .format(secrets.azure['tenant_id'])
        
        response = self._https.post(url, data=data)
        print("status: ", response.status_code)

        json_resp = response.json()
        try:
            token = json_resp["access_token"]
        except KeyError as error:
            self._error_handler(error)
            quit()

        return token