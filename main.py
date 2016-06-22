#!/usr/bin/env python
"""
		schluknik 2016
		run with python 2.7.6
"""

####    Author Information      ####

__author__ = "Elias Kardel"
__copyright__ = "Copyright 2016t"
__credits__ = ["Elias Kardel"]
__license__ = "GPL"
__maintainer__ = "Elias Kardel"
__email__ = "elias.kardel@u-blox.com"
__status__ = "development"

###     Imports     ###

import kivy
kivy.require('1.8.7')

import kivy
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

###     kv integration     ###

Builder.load_string("""
<CityButton@Button>:
    color: 1,1,1,1
    font_size: 32
    

<FTPButton@Button>:
    color: 1,1,1,1
    font_size: 32
 
<MyBoxLayout@BoxLayout>:
    orientation: 'vertical'
    padding: 30,30,30,30
    spacing: 5           

<CityScreen>:
    MyBoxLayout:
        Image:
            source: 'city.png'
        CityButton:
            text: 'Prenzlauer-Berg'
            on_press: root.manager.current = 'beer'
        CityButton:
            text: 'Friedrichshain'
            on_press: root.manager.current = 'beer'
<BeerScreen>:
    grid: Grid
    MyBoxLayout:
        Image:
            source: 'beer.png'
        Slider:
            id: slider_id
            min: 0
            step: 0.01
            max: 10
            on_touch_up: root.manager.current = 'hang'
            on_value: root.addbeer(slider_id.value)
        Label:
            text: str(round(slider_id.value, 1))
            color: 0,0,0,1
        GridLayout:
            id: Grid
            cols: 10
            rows: 1
<HangScreen>:
    grid: Grid
    MyBoxLayout:
        Image:
            source: 'hang.png'
            scale: 2.0
        Slider:
            id: slider_id
            min: 0
            step: 0.01
            max: 10
            on_touch_up: root.manager.current = 'result'
            on_value: root.addpoop(slider_id.value)
        Label:
            text: str(round(slider_id.value, 0))
            color: 0,0,0,1
        GridLayout:
            id: Grid
            cols: 10
            rows: 1
<ResultScreen>:
    MyBoxLayout:
        Image:
            source: 'result.png'
""")

###     Screen Declaration     ####    

class SettingsScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class CityScreen(Screen):
    pass

class HangScreen(Screen):

    def addpoop(instance, value):
        """
		Button pressed handler
        """
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='poop.png')
            instance.grid.add_widget(wimg)
    pass

class BeerScreen(Screen):

    def addbeer(instance, value):
        """
		Button pressed handler
        """
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='beerchen.jpg')
            instance.grid.add_widget(wimg)
    pass

    def callback(instance, event):
        """
		Button pressed handler
        """
        # File FTP transfer
		# domain name or server ip:
        ftp = FTP('singing-wires.de')
		# how to encrypt this?
        ftp.login(user='web784', passwd = 'Holz0815')
        ftp.cwd('/html/schluknik')
        filename = event.text + ".txt"
		# todo: store as .csv file
        with open(filename,"a+") as f:		
            ftp.storlines("STOR " + filename, open(filename, 'r'))
            ftp.quit()
            print('sucessfully created file'+ filename)
        instance.disabled = True
    pass

# create the screen manager
sm = ScreenManager()
sm.add_widget(CityScreen(name='city'))
sm.add_widget(BeerScreen(name='beer'))
sm.add_widget(ResultScreen(name='result'))
sm.add_widget(HangScreen(name='hang'))

###     Body        ###
class Myapp(App):
    """
    Main class
    """
    def build(self):
        """
		Layout builder of main window
        """
        # set bg color to white
        Window.clearcolor = (1, 1, 1, 0)

        # load start screen
        #startscreen = CityScreen()
        return sm 

###    entry point      ####
if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
