##### SNAPSHOT #####
# A life snapshot of goals, quotes and countdown to bliss

# Imports
import board
import time
import math
import json
import alarm
from adafruit_magtag.magtag import MagTag

# Modules
from countdown.countdown import Countdown
from goals.goals import Goals
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
  "goals": 1,
  "quotes": 2,
}

# Initializers
countdown = Countdown()
goals = Goals()
quotes = Quotes()

# Number of active modules
active_module = 1
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
    if active_module == modules["goals"]:
        print('refreshing goals')
        goals.refresh(magtag)
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
        goals.update(magtag)
        quotes.update(magtag)

        magtag.peripherals.neopixel_disable = True

    except (ValueError, RuntimeError) as e:
        magtag.set_text(e)
        print("Some error occured, retrying later -", e)


# Store module data on the RAM
def store_data():
    data = {
        "module": active_module,
    }
    countdown.save_data(data)
    goals.save_data(data)
    quotes.save_data(data)

    dump = json.dumps(data).encode('utf-8')
    
    mem_size = len(dump)
    n = math.floor(mem_size/255)
    m = mem_size % 255
    alarm.sleep_memory[0] = n
    alarm.sleep_memory[1] = m
    alarm.sleep_memory[2:mem_size+2] = dump


# Load data stored on the RAM
def load_data():
    mem_size = 255 * alarm.sleep_memory[0] + alarm.sleep_memory[1]
    data = json.loads(alarm.sleep_memory[2:mem_size+2].decode('utf-8'))
    
    global active_module
    active_module = data["module"]
    countdown.load_data(data)
    goals.load_data(data)
    quotes.load_data(data)


#####################
##### OPERATION #####
#####################

# if just starting
if not alarm.wake_alarm:
    update_modules()
    refresh_display()

# if waking up from a time alarm
elif isinstance(alarm.wake_alarm, alarm.time.TimeAlarm):
    load_data()
    update_modules()
    refresh_display()

# if waking up from a pin alarm
elif isinstance(alarm.wake_alarm, alarm.pin.PinAlarm):
    # audio and visual feedback
    magtag.peripherals.play_tone(AWAKE_TONE, 0.1)
    
    load_data()

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
store_data()

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
