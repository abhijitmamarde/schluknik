#!/usr/bin/env python
"""
		schluknik 2016
		run with python 2.7.6
"""

################################################################################################

####    Author Information      ####

###############################################################################################

__author__ = "Elias Kardel"
__copyright__ = "Copyright 2016t"
__credits__ = ["Elias Kardel"]
__license__ = "GPL"
__maintainer__ = "Elias Kardel"
__email__ = "elias.kardel@u-blox.com"
__status__ = "development"

################################################################################################

###    Imports    ####

###############################################################################################

# imports from subfolders
#from geartick import *
# for gps access 
from plyer import gps
# notification
from plyer import notification
# maps
from mapview import *
# for graph 
from graph import *
# for pizza graph
from pizza import *

# widget import all python classes
from widgets import BackgroundScreenManager
from widgets import DrinkScreen
from widgets import SettingsScreen
from widgets import DestroyScreen
from widgets import HealScreen
from widgets import FeelScreen
from widgets import ResultScreen
from setcard import setcard
from widgets import settings

from widgets.settingsjson import settings_json

# kivy importd
import kivy
kivy.require('1.8.7')
from kivy.event import EventDispatcher
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation 
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from ftplib import FTP
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.slider import Slider
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.bubble import Bubble
from kivy.utils import get_color_from_hex as rgb

from kivy.uix.settings import Settings, SettingItem, SettingsPanel, SettingTitle

# import other stuff
import os.path

# import python natives
# for date and time stamp
import datetime
import numpy as numpy
import csv
import traceback
import io
import json
import re
import ConfigParser

# 
from glob import glob 
from os.path import dirname, join, basename
from kivy.core.text import Label
from kivy.core.text import LabelBase
from kivy.core.text import LabelBase


################################################################################################

###    KV Integration    ####

################################################################################################

def load_all_kv_files(start="./widgets"):
    '''
    sources all files with *.kv ending in ./widget directory
    '''
    pattern = re.compile(r".*?\.kv")
    kv_files = []
    for root, dirs, files in os.walk(start):
        kv_files += [root + "/" + file_ for file_ in files if pattern.match(file_)]

    for file_ in kv_files:
        Builder.load_file(file_)

################################################################################################

###     globals     ####  

################################################################################################

setc = setcard();

# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

# font integration
KIVY_FONTS = [
    {
        "name": "RobotoCondensed",
        "fn_regular": "data/fonts/RobotoCondensed-Light.ttf",
        "fn_bold": "data/fonts/RobotoCondensed-Regular.ttf",
        "fn_italic": "data/fonts/RobotoCondensed-LightItalic.ttf",
        "fn_bolditalic": "data/fonts/RobotoCondensed-Italic.ttf"
    }
]

for font in KIVY_FONTS:
    LabelBase.register(**font)
################################################################################################

###     Todo: remove below     ####

################################################################################################

class ColorDownButton(Button):
    """
    Button with a possibility to change the color on on_press (similar to background_down in normal Button widget)
    """
    background_color_normal = ListProperty([1, 1, 1, 0.5])
    background_color_down = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super(ColorDownButton, self).__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = self.background_color_normal

    def on_press(self):
        self.background_color = self.background_color_down

    def on_release(self):
        self.background_color = self.background_color_normal

################################################################################################

###    Body     ####

################################################################################################

class Myapp(App):
    """
    Main class
    """
    KIVY_DEFAULT_FONT = "RobotoCondensed"

    #manager = ObjectProperty()
    #settings_cls = SettingsScreen.KognitivoSettings

    global_location = StringProperty()
    # some random intitial location
    lat = 19.0
    lon = 72.48
    gps_status = StringProperty('Click Start to get GPS location updates')

    @mainthread
    def on_location(self, **kwargs):
        self.global_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        self.lat = float('{lat}'.format(**kwargs))
        self.lon = float('{lon}'.format(**kwargs))

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def build(self):
        """
		Layout builder of main window
        """

        # load all kv files 
        load_all_kv_files()

        # set bg color to white
        #notification.notify('test tiltle','scanning started')
        #Window.clearcolor = (1, 1, 1, 0)
        self.gps = gps
        try:
            # get gps coordinates
            self.gps.configure(on_location=self.on_location,
                               on_status=self.on_status)
            self.gps.start()
        except NotImplementedError:
            # if running on PC
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'
            self.lat = float(19.0)
            self.lon = float(72.48)
            self.alki_score = ""
       # try: 

        # create the screen manager
        self.sm = BackgroundScreenManager.BackgroundScreenManager()
        # check the seetings config
        config = ConfigParser.ConfigParser()
        config.read('myapp.ini')
        self.smoker = config.getboolean('personaldata','smoker')  
        self.gender = config.get('personaldata','gender') 
        self.age =  config.getint('personaldata','age')  
        self.height = config.getint('personaldata','height') 
        self.weight = config.getint('personaldata','weight')

        self.sm.add_widget(DrinkScreen.DrinkScreen(name='drink'))
                
        # adding all the sub screens to the screen handler
        self.sm.add_widget(DestroyScreen.DestroyScreen(name='destroy'))
        self.sm.add_widget(HealScreen.HealScreen(name='heal'))
        #self.sm.add_widget(FeelScreen.FeelScreen(name='feel'))
        self.sm.add_widget(ResultScreen.ResultScreen(name='result'))

        # loading in data from server before starting the app
        # filename of global performance data
        filename = "schlukniktable.csv"
        # File FTP transfer
		# domain name or server ip:
        ftp = FTP('singing-wires.de')
		# todo: how to encrypt this?
        ftp.login(user='web784', passwd = 'Holz0815')
        ftp.cwd('/html/schluknik')
        # gets the file from the server and stores it locally
        try:  
            gFile = open(filename, "wb")
            ftp.retrbinary("RETR " + filename ,gFile.write)
            ftp.quit()
            gFile.close()
            self.global_history = numpy.genfromtxt(filename, delimiter=';', dtype='string')
        except:
            tb = traceback.format_exc()
            print (tb)

        ## loading local history before start up
        # file name for the history file
        fname_history = 'history.csv' 
        # check if it exists
        if(os.path.isfile(fname_history)):
             self.personal_history = numpy.genfromtxt(fname_history, delimiter=';', dtype='string') 
        # create the screen manager instance
        return self.sm

    # for settings screen
    def build_config(self, config):
        config.setdefaults('personaldata', {
        'name': 'Elias',
        'smoker': True,
        'age': 28,
        'height': 185,
        'weight': 70,
        'gender': 'boy'})

    def build_settings(self, settings):
        settings.add_json_panel('schluknik settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

################################################################################################

###    Entry point     ####

################################################################################################

if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
