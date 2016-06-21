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

###     kv integration     ###

Builder.load_string("""
<CityButton@Button>:
    color: 1,1,1,1
    font_size: 32
    

<FTPButton@Button>:
    color: 1,1,1,1
    font_size: 32
    on_press: self.parent.parent.callback
    

<CityScreen>:
    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'start.png'
        CityButton:
            text: 'Prenzlauer-Berg'
            on_press: root.manager.current = 'beer'
        CityButton:
            text: 'Friedrichshain'
            on_press: root.manager.current = 'beer'

<BeerScreen>:
    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'start.png'
        FTPButton:
            text: '1'
            on_press: root.manager.current = 'result'
        FTPButton:
            text: '2'
            on_press: root.manager.current = 'result'
        FTPButton:
            text: '3'
        FTPButton:
            text: '4'
        FTPButton:
            text: '5'
        FTPButton:
            text: '6'
<ResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        Image:
            source: 'stable.png'

        
""")

###     Screen Declaration     ####    

class SettingsScreen(Screen):
    pass

class ResultScreen(Screen):
    pass

class CityScreen(Screen):
    pass

class BeerScreen(Screen):

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
