##### SNAPSHOT #####
# A life snapshot of goals, quotes and countdown to bliss

import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests

import board
import time
import math
import alarm
from adafruit_magtag.magtag import MagTag
from digitalio import DigitalInOut, Direction, Pull

# Modules
from countdown.countdown import Countdown
from quotes.quotes import Quotes

# Constants
BUTTON_AWAKE_TIME = 15
REFRESH_TIME_IN_MINS = 15

AWAKE_TONE = 100
BUTTON_TONE = 1568

UPDATE_COLOR = (255, 0, 0)
REFRESH_COLOR = (255, 255, 255)

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
magtag_pixels = magtag.peripherals.neopixels
magtag_pixels.brightness = 0.1

##### Functions #####

# Refresh the display
def refresh_display():
    magtag.peripherals.neopixel_disable = False
    magtag.peripherals.neopixels.fill(REFRESH_COLOR)

    if active_module == modules["countdown"]:
        print('refreshing count')
        countdown.refresh(magtag)
    if active_module == modules["quotes"]:
        print('refreshing quotes')
        quotes.refresh(magtag)

    magtag.peripherals.neopixel_disable = True


# Update modules data
def update_modules():    
    try:
        magtag.peripherals.neopixel_disable = False
        magtag.peripherals.neopixels.fill(UPDATE_COLOR)

        magtag.network.connect()
        countdown.update(magtag)
        quotes.update(magtag)

        magtag.peripherals.neopixel_disable = True

    except (ValueError, RuntimeError) as e:
        magtag.set_text(e)
        print("Some error occured, retrying later -", e)


#####################
##### OPERATION #####
#####################

# if just starting
if not alarm.wake_alarm:
    update_modules()
    refresh_display()

# if waking up from a time alarm
elif isinstance(alarm.wake_alarm, alarm.time.TimeAlarm):
    active_module = alarm.sleep_memory[0]
    update_modules()
    refresh_display()

# if waking up from a pin alarm
elif isinstance(alarm.wake_alarm, alarm.pin.PinAlarm):
    # audio and visual feedback
    magtag.peripherals.play_tone(AWAKE_TONE, 0.1)
    
    active_module = alarm.sleep_memory[0]
    update_modules()
    
    if alarm.wake_alarm.pin is board.BUTTON_A:
        active_module = (active_module - 1) % len(modules)
        change_module = True
    elif alarm.wake_alarm.pin is board.BUTTON_D:
        active_module = (active_module + 1) % len(modules)
        change_module = True

    wake_time = time.monotonic()
    while (time.monotonic() - wake_time) < BUTTON_AWAKE_TIME:
        # Cycle through the active module
        if magtag.peripherals.button_d_pressed:
            magtag.peripherals.play_tone(BUTTON_TONE, 0.1)
            active_module = (active_module + 1) % len(modules)
            change_module = True
        if magtag.peripherals.button_a_pressed:
            magtag.peripherals.play_tone(BUTTON_TONE, 0.1)
            active_module = (active_module - 1) % len(modules)
            change_module = True
        
        if change_module:
            change_module = False
            refresh_display()
            wake_time = time.monotonic()


#################
##### SLEEP #####
#################

# Store module data
alarm.sleep_memory[0] = active_module

# Set the pin alarms
magtag.peripherals.deinit()
pin_alarm_1 = alarm.pin.PinAlarm(pin=board.BUTTON_A, value=False, pull=True)
pin_alarm_2 = alarm.pin.PinAlarm(pin=board.BUTTON_D, value=False, pull=True)

# Calculate seconds passed since midnight
now = time.localtime()
hour, minutes, seconds = now[3:6]
seconds_since_midnight = 60 * (hour * 60 + minutes) + seconds

# Set time alarm to wake up some minutes after midnight
seconds_to_sleep = (24 * 60 * 60 - seconds_since_midnight) + REFRESH_TIME_IN_MINS * 60
print(
    "Sleeping for {} hours, {} minutes".format(
        seconds_to_sleep // 3600, (seconds_to_sleep // 60) % 60
    )
)
time_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic() + seconds_to_sleep)

# Put the board to deep sleep
alarm.exit_and_deep_sleep_until_alarms(time_alarm, pin_alarm_1, pin_alarm_2)
