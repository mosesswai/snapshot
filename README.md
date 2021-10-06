# Snapshot
A daily life updater based on Adafruit's MagTag

## Hardware
- [Adafruit Magtag Starter Kit](https://www.adafruit.com/product/4819)
  - 1 x [Adafruit Magtag](https://www.adafruit.com/magtag) - A 2.9" (296 x 128 pixels) grayscale E-Ink display with a ESP32-S2 wireless module
  - 1 x [Li-ion polymer battery 3.7V 420mAh](https://www.adafruit.com/product/4236)
  - 4 x [Mini magnet feet](https://www.adafruit.com/product/4631)

## Software

### Behavior
The displays starts with the default active module when powered up. The device fetches data needed for all modules and enters deep sleep mode. In this mode it consumes minimal power to prolong the battery life. The device can be awaken from deep sleep by pressing the *forward* or *back* buttons which will cycle the active module on display. It will stay awake for 30s after the last button press and re-enter deep sleep. Each module's relevant data is saved when the device enters sleep mode and retreived when woken up.

At midnight, the device will fetch data to update all modules and refresh the display.

For some HMI, the LEDs on top act as status lights, red when fetching data from the internet and white when refreshing the display. *The device can not be interacted with when the status lights are on.*

The top level module, [code.py](code.py) is the controller that is responsible for 
- Cycling between active modules  
- Power management
- Loading and saving module data

### Modules
1. [Countdown](countdown/countdown.py) - Displays time left to reach a target date and time.
    
    The target is set on a Google Sheet and accessed via [Google Sheets API](https://developers.google.com/sheets/api). The display will show how many days are left until the countdown is less than 48 hours, where it switches to hours.
    
    <img src="https://user-images.githubusercontent.com/18386420/136146048-0c647062-4361-4d33-a094-da48bdbc430f.jpg" width=30% height=30%>

2. [Goals](goals/goals.py) - Displays the level of accomplishment of a set of goals

    The target goal and current state are both manually updated on a Google Sheet
    
    <img src="https://user-images.githubusercontent.com/18386420/136144718-66219c81-fae6-4b8c-a9d9-d6e3c29d0d72.jpg" width=30% height=30%>


3. [Quotes](quotes/quotes.py) - Displays a random quote from [Adafruit's Quotes API]("https://www.adafruit.com/api/quotes.php")
    
    <img src="https://user-images.githubusercontent.com/18386420/136145994-1910078e-2117-4a16-ba2f-d127f1bb4bcc.jpg" width=30% height=30%>


### Privacy
The project stores sensitive information like WiFi passwords, tokens and API keys in a file called **secrets.py** that is not public (following [Adafruits' CircuitPython framework recommendation](https://learn.adafruit.com/adafruit-magtag/internet-connect)). In this fashion, the actual Google Sheet URLs are stored in secrets.py. The URL format is:
```
https://sheets.googleapis.com/v4/spreadsheets/*google_sheet_code*/values/*spreadsheet_tab_name*?alt=json&key=*API_key*
```
