# Goals dashboard and quotes displayer

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

import time
import math
from adafruit_magtag.magtag import MagTag
from digitalio import DigitalInOut, Direction, Pull

# Modules
from countdown.countdown import Countdown

# Constants
TIME_BETWEEN_REFRESHES = 5

magtag = MagTag()

# # Set up where we'll be fetching data from
# DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
# QUOTE_LOCATION = [0, "text"]
# AUTHOR_LOCATION = [0, "author"]
# # in seconds, we can refresh about 100 times on a battery
# TIME_BETWEEN_REFRESHES = 1 * 60 * 60  # one hour delay

# magtag = MagTag(
#     url=DATA_SOURCE,
#     json_path=(QUOTE_LOCATION, AUTHOR_LOCATION),
# )

# Number of active modules
modules = [
    "goals",
    "quotes",
    "bunny"
]

module_id = 0
module_change = False


# Modules
countdown = Countdown()


def refresh_display():
    countdown.refresh(magtag)


def update_modules():    
    # refresh 'bunny'
    try:
        magtag.network.connect()
        countdown.update(magtag)

    except (ValueError, RuntimeError) as e:
        magtag.set_text(e)
        print("Some error occured, retrying later -", e)

    # magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)


#####################
##### MAIN LOOP #####
#####################

while True:
    # Cycle through the active module
    if magtag.peripherals.button_d_pressed:
        module_id = (module_id + 1) % len(modules)
        module_change = True
    if magtag.peripherals.button_a_pressed:
        module_id = (module_id - 1) % len(modules)
        module_change = True
    
    if module_change:
        module_change = False
        update_modules()
        refresh_display()

