#################
##### Goals #####
#################

# Imports
import time
from adafruit_progressbar.progressbar import ProgressBar
import secrets

class Goals:

    # Constants
    BACKGROUND = 0x999999

    # Sheet data URL (JSON)
    SOURCE_URL = secrets.monthly_goals_source_url
    data = None

    ##### Initializer #####
    def __init__(self):
        pass


    ##### Refresher #####
    def refresh(self, magtag):
        # Bad practice, clears the splash text and empties the text cache in PortalBase
        if len(magtag.splash) > 1:
            for i in range(len(magtag.splash)-1):
                magtag.splash.pop(-1)
        magtag._text = []

        magtag.graphics.set_background(self.BACKGROUND)

        # Calculate the number of data rows
        num_rows = len(self.data)-1

        # Add the heading text object
        magtag.add_text(
            text_font="/fonts/MontserratAlternates-Bold-24.bdf",
            text_position=((magtag.graphics.display.width // 2), 11),
            text_scale=1,
            text_anchor_point=(0.5, 0.5),
            is_data=False,
        )
        
        magtag.set_text("Goals", 0, auto_refresh=False)

        # Set display components location parameters
        X_TEXT = 8
        X_BAR = 105
        Y_START = 28
        BAR_WIDTH = 180
        BAR_HEIGHT = int(100 / num_rows) - 5
        
        # Calculate the y anchor point for the text labels 
        if num_rows <= 2:
            Y_ANCHOR = 0
        else:
            Y_ANCHOR = (num_rows-2) * 0.1
        
        # Add the text label and progress bar objects for each data row
        for i in range(1,len(self.data)):
            
            # Set the y position for each component relative to the bar height
            Y = Y_START + (i-1) * (BAR_HEIGHT+5)

            # Create a new text label object
            magtag.add_text(
                text_font="/fonts/MontserratAlternates-Medium-22.bdf",
                text_position=(X_TEXT, Y),
                text_scale=1,
                text_anchor_point=(0, Y_ANCHOR),
                is_data=False,
            )

            magtag.set_text(self.data[i][0], i, auto_refresh=False)

            # Create a new progress_bar object
            progress_bar = ProgressBar(
                X_BAR, Y, BAR_WIDTH, BAR_HEIGHT, 1.0, bar_color=0x999999, outline_color=0x000000
            )

            magtag.graphics.splash.append(progress_bar)

            # Calculate the progress bar value
            progress_bar.progress = float(self.data[i][2])/float(self.data[i][1])
            

        # wait 2 seconds for display to complete
        magtag.refresh()
        time.sleep(2)


    ##### Updater #####
    def update(self, magtag):
        response = magtag.network.fetch(self.SOURCE_URL)
        if response.status_code == 200:
            entries = response.json()['values']
            self.data = entries


    ##### OLD MICROSOFT GRAPH API CODE #####
    # def __init__(self):
    #     wifi.radio.connect(secrets.secrets['ssid'], secrets.secrets['password'])

    #     pool = socketpool.SocketPool(wifi.radio)
    #     self._https = requests.Session(pool, ssl.create_default_context())

    #     try:
    #         token = self._get_token()
    #     except (ValueError, RuntimeError) as e:
    #         print("Some error occured, retrying later -", e)
        
    #     headers = {'Authorization': 'Bearer ' + token}

    #     url = 'https://graph.microsoft.com/v1.0/me/onenote/pages'

    #     response = self._https.get(url, headers=headers)
    #     print(response.status_code)

    #     json_resp = response.json()
    #     print(json_resp)


    # # Fetch access token
    # def _get_token(self):
    #     data = {'grant_type': 'client_credentials',
    #             # 'grant_type': 'password',
    #             # 'username':'xxxx',
    #             # 'password':'xxxx',
    #             'client_id': secrets.azure['app_id'],
    #             'client_secret': secrets.azure['client_secret'],
    #             'scope': 'https://graph.microsoft.com/.default',
    #             'resource': 'https://graph.microsoft.com/'
    #             }
    #     url = 'https://login.microsoftonline.com/{}/oauth2/token'\
    #           .format(secrets.azure['tenant_id'])
        
    #     response = self._https.post(url, data=data)
    #     print("status: ", response.status_code)

    #     json_resp = response.json()
    #     try:
    #         token = json_resp["access_token"]
    #     except KeyError as error:
    #         self._error_handler(error)
    #         quit()

    #     return token