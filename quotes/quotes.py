##########################
###### Quotes Module #####
##########################

# Imports
import time

class Quotes:
    # Constants
    BACKGROUND = "/quotes/quotes_bg.bmp"
    DATA_SOURCE = "https://www.adafruit.com/api/quotes.php"
    QUOTE_LOCATION = [0, "text"]
    AUTHOR_LOCATION = [0, "author"]

    # Variables
    quote = ""
    author = ""

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
        
        # quote in bold text, with text wrapping
        magtag.add_text(
            text_font="/fonts/Arial-Bold-12.bdf",
            text_wrap=28,
            text_maxlen=120,
            text_position=(
                (magtag.graphics.display.width // 2),
                (magtag.graphics.display.height // 2) - 10,
            ),
            line_spacing=0.75,
            text_anchor_point=(0.5, 0.5),  # center the text on x & y
            is_data=False,
        )
        
        # author in italic text, no wrapping
        magtag.add_text(
            text_font="/fonts/Arial-Italic-12.bdf",
            text_position=(magtag.graphics.display.width // 2, 118),
            text_anchor_point=(0.5, 0.5),  # center it in the nice scrolly thing
            is_data=False,
        )

        # Set the text objects
        magtag.set_text(self.quote, 0, auto_refresh=False)
        magtag.set_text(self.author, 1, auto_refresh=False)

        # wait 2 seconds for display to complete
        magtag.refresh()
        time.sleep(2)
    

    ##### Updater #####
    def update(self, magtag):
        magtag.json_path=(self.QUOTE_LOCATION, self.AUTHOR_LOCATION)
        value = magtag.fetch(refresh_url=self.DATA_SOURCE, timeout=10, auto_refresh=False)

        self.quote = value[0]
        self.author = value[1]
