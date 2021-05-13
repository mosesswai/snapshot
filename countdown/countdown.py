# Countdown Module

# Imports
import time
import math
import terminalio

class Countdown:
    # Constants
    SECONDS_IN_HOUR = 3600 
    HOURS_IN_A_DAY = 24
    HOURS_TO_DAYS_THRESHOLD = 48
    BACKGROUND = "/countdown/countdown_bg.bmp"

    # Variables
    time_target = time.struct_time((2021, 5, 25, 7, 0, 0, 1, 145, -1))
    time_diff = 0


    ##### Initializer #####
    def __init__(self):
        pass
    

    ##### Refresher #####
    def refresh(self, magtag):
        magtag.graphics.set_background(self.BACKGROUND)

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

        diff = self.time_diff
        if diff > self.HOURS_TO_DAYS_THRESHOLD:
            magtag.set_text(math.ceil(diff/self.HOURS_IN_A_DAY), 0, auto_refresh=False)
            magtag.set_text("days", 1, auto_refresh=False)
        else:
            magtag.set_text(math.ceil(diff), 0, auto_refresh=False)
            magtag.set_text("hours", 1, auto_refresh=False)
        
        # wait 2 seconds for display to complete
        time.sleep(2)


    ##### Updater #####
    def update(self, magtag):
        # get time from the network
        magtag.get_local_time()
        now = time.localtime()
        self.time_diff = ( time.mktime(self.time_target) - time.mktime(now) ) / self.SECONDS_IN_HOUR