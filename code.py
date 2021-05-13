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
from quotes.quotes import Quotes

# Constants
TIME_BETWEEN_REFRESHES = 5

####################
###### Modules #####
####################

# Names
modules = {
  "countdown": 0,
  "quotes": 1,
}

# Initializers
countdown = Countdown()
quotes = Quotes()

# Number of active modules
active_module = 0
change_module = False

################
##### Main #####
################

magtag = MagTag()

##### Functions #####

# Refresh the display
def refresh_display():
    if active_module == modules["countdown"]:
        print('refreshing count')
        countdown.refresh(magtag)
    if active_module == modules["quotes"]:
        print('refreshing quotes')
        quotes.refresh(magtag)


# Update modules data
def update_modules():    
    try:
        magtag.network.connect()
        countdown.update(magtag)
        quotes.update(magtag)

    except (ValueError, RuntimeError) as e:
        magtag.set_text(e)
        print("Some error occured, retrying later -", e)

    # magtag.exit_and_deep_sleep(TIME_BETWEEN_REFRESHES)


#####################
##### LOOP #####
#####################

while True:
    # Cycle through the active module
    if magtag.peripherals.button_d_pressed:
        active_module = (active_module + 1) % len(modules)
        change_module = True
    if magtag.peripherals.button_a_pressed:
        active_module = (active_module - 1) % len(modules)
        change_module = True
    
    if change_module:
        change_module = False
        update_modules()
        refresh_display()
