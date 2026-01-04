#############################
###### Countdown Module #####
#############################

# Imports
import time
import math
import terminalio
import secrets

class Workout:
    # Constants
    SECONDS_IN_HOUR = 3600 
    HOURS_IN_A_DAY = 24
    HOURS_TO_DAYS_THRESHOLD = 48
    # BACKGROUND = "/workout/workout_bg.bmp"
    BACKGROUND = 0x999999

    # Variables
    SOURCE_URL = secrets.workout_source_url
    day = ""
    soccer = ""
    group = ""
    

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

        # Determine the text values
        if self.group == "G1":
            text_workout = "Biceps, Chest"
        elif self.group == "G2":
            text_workout = "Triceps, Back, Spin"
        elif self.group == "G3":
            text_workout = "Shoulder, Abs, Run"
        elif self.group == "G4":
            text_workout = "Legs, Rope"
        elif self.group == "Rest":
            text_workout = "Triceps, Back, Spin"

        # Add the text objects
        magtag.add_text(
            text_font = "/fonts/Arial-Bold-12.bdf",
            text_position = ((magtag.graphics.display.width * 0.5), 30),
            text_scale = 2,
            text_anchor_point = (0.5, 0.5),
            is_data = False,
        )
        
        magtag.add_text(
            text_font = terminalio.FONT,
            text_position = ((magtag.graphics.display.width * 0.5), 80),
            # text_wrap = 15,
            text_scale = 2,
            text_anchor_point = (0.5, 0.5),
            is_data = False,
        )

        # magtag.add_text(
        #     text_font = terminalio.FONT,
        #     text_position = ((magtag.graphics.display.width * 0.5), 110),
        #     text_scale = 2,
        #     text_anchor_point = (0.5, 0.5),
        #     is_data = False,
        # )

        # Set the text objects
        magtag.set_text(self.day, 0, auto_refresh=False)
        magtag.set_text(text_workout, 1, auto_refresh=False)
        # magtag.set_text(self.soccer, 2, auto_refresh=False)


        # wait 2 seconds for display to complete
        magtag.refresh()
        time.sleep(2)
    

    ##### Updater #####
    def update(self, magtag):
        # get the time target
        response = magtag.network.fetch(self.SOURCE_URL)
        if response.status_code == 200:
            entries = response.json()['values']

        # get current week number from the network
        magtag.get_local_time()
        now = time.localtime()
        week_day = now.tm_wday
        week_num = math.ceil((now.tm_yday+3)/7)

        # determine the weekday
        if week_day == 0: self.day = "Monday"
        elif week_day == 1: self.day = "Tuesday"
        elif week_day == 2: self.day = "Wednesday"
        elif week_day == 3: self.day = "Thursday"
        elif week_day == 4: self.day = "Friday"
        elif week_day == 5: self.day = "Saturday"
        elif week_day == 6: self.day = "Sunday"

        # determine the workout group
        self.soccer = entries[week_num][1]
        if self.soccer == "Tuesday": workout_row = 1
        elif self.soccer == "Wednesday": workout_row = 2
        elif self.soccer == "Thursday": workout_row = 3
        else: workout_row = 0
        
        self.group = entries[workout_row][week_day+4]

    
    ##### Saver #####
    def save_data(self, data_dict):
        data = {
            "day": self.day,
            "soccer": self.soccer,
            "group": self.group
        }
        data_dict["workout"] = data


    ##### Loader #####
    def load_data(self, data_dict):
        data = data_dict["workout"]
        self.day = data["day"]
        self.soccer = data["soccer"]
        self.group = data["group"]
        