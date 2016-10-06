from kivy.utils import get_color_from_hex 

# general
KIVY_VERSION_REQUIRE = '1.8.0'  
KIVY_GRAPHICS_HEIGHT = None  
KIVY_GRAPHICS_WIDTH = None  
KIVY_LOG_LEVEL = "info"

# database
DATABASE_DEBUG = False  
DATABASE_ADDRESS = 'sqlite:///db.sqlite3'

#screens
ACTIVITY_SHOW_STATS_PERIOD = 30  # days

# test flight
TESTFLIGHT_TOKEN = None

# tasks
ACTIVE_TASK_CLASSES = []  
INACTIVE_TASK_CLASSES = []  
INTRO_HINT_LENGTH = 5  

#try:  
#    platform_settings = "from settings_" + platform() + " import *"
#    exec platform_settings
#except ImportError:  
#    pass

KIVY_FONTS = [  
    {
        "name": "RobotoCondensed",
        "fn_regular": "data/fonts/RobotoCondensed-Light.ttf",
        "fn_bold": "data/fonts/RobotoCondensed-Regular.ttf",
        "fn_italic": "data/fonts/RobotoCondensed-LightItalic.ttf",
        "fn_bolditalic": "data/fonts/RobotoCondensed-Italic.ttf"
    },
    {
        "name": "FreeSerif",
        "fn_regular": "data/fonts/FreeSerif.ttf"
    }
]

KIVY_DEFAULT_FONT = "RobotoCondensed"
TEXT_COLOR = get_color_from_hex("666666ff")  
TEXT_COLOR_SEMITRANSPARENT = get_color_from_hex("66666680")  
FILL_COLOR = get_color_from_hex("7e7edcff")  
FILL_COLOR_SEMITRANSPARENT = get_color_from_hex("7e7edc80")  
FILL_COLOR_QUASITRANSPARENT = get_color_from_hex("7e7edc33")