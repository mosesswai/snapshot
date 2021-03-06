#############################
###### Countdown Module #####
#############################

# Imports
import time
import math
import terminalio
import secrets

class Countdown:
    # Constants
    SECONDS_IN_HOUR = 3600 
    HOURS_IN_A_DAY = 24
    HOURS_TO_DAYS_THRESHOLD = 48
    BACKGROUND = "/countdown/countdown_bg.bmp"

    # Variables
    SOURCE_URL = secrets.countdown_source_url
    time_diff = 0
    

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

        # Calculate the text values
        diff = self.time_diff
        if diff > self.HOURS_TO_DAYS_THRESHOLD:
            text_number = math.floor(diff/self.HOURS_IN_A_DAY)
            text_unit = "days"
        else:
            text_number = math.floor(diff)
            if text_number < 0:
                text_number = 0
            text_unit = "hours"

        # Add the text objects
        magtag.add_text(
            text_font=terminalio.FONT,
            text_position=((magtag.graphics.display.width * 0.75), 35),
            text_scale=7,
            text_anchor_point=(0.5, 0.5),
            is_data=False,
        )
        
        magtag.add_text(
            text_font=terminalio.FONT,
            text_position=( (magtag.graphics.display.width * 0.75), 90),
            text_scale=4,
            text_anchor_point=(0.5, 0.5),
            is_data=False,
        )

        # Set the text objects
        magtag.set_text(text_number, 0, auto_refresh=False)
        magtag.set_text(text_unit, 1, auto_refresh=False)

        # wait 2 seconds for display to complete
        magtag.refresh()
        time.sleep(2)
    

    ##### Updater #####
    def update(self, magtag):
        # get the time target
        response = magtag.network.fetch(self.SOURCE_URL)
        if response.status_code == 200:
            entries = response.json()['values']
            target = list(map(int, entries[1]))
            time_target = time.struct_time((target[0], target[1], target[2], 
                                            target[3], target[4], target[5], 
                                            0, -1,-1))

        # get current time from the network
        magtag.get_local_time()
        now = time.localtime()
        self.time_diff = ( time.mktime(time_target) - time.mktime(now) ) / self.SECONDS_IN_HOUR

    
    ##### Saver #####
    def save_data(self, data_dict):
        data = {
            "diff": self.time_diff
        }
        data_dict["countdown"] = data


    ##### Loader #####
    def load_data(self, data_dict):
        data = data_dict["countdown"]
        self.time_diff = data["diff"]
        