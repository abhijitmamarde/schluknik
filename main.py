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
kivy.require('1.0.7')

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from ftplib import FTP
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window

###     Body        ###
class VBoxLayoutExample(App):
    """
    Main class
    """
    def setOrientation(self, orient):
        """
		Todo
        """
        self.orient = orient

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
    
    def build(self):
        """
		Layout builder of main window
        """
        self.icon = 'icon.png'
        Window.clearcolor = (1, 1, 1, 0)	
        layout = BoxLayout(padding=10, orientation=self.orient)
        l = Label(text='[color=ff3333]Where have you been last night?[/color]',markup = True, font_size='20sp')
        l.bind(texture_size=l.setter('size'))
        layout.add_widget(l)
        wimg = Image(source='stable.png')
        layout.add_widget(wimg)
        zone = ['PBerg', 'Friedrichshain', 'Mitte', 'Kreuzberg', 'Lichtenberg']
        for i in zone:
			btn = Button(text= str(i))
			btn.bind(on_press=self.callback)
			layout.add_widget(btn)
        return layout

###     Class section       ###
class RootScreen(ScreenManager):
    pass
class StartScreen(FloatLayout):

	def __init__(self, **kwargs):
		super(StartScreen, self).__init__(**kwargs)
class TestApp(App):
  
	def build(self):
		
		return StartScreen()

#######
if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = VBoxLayoutExample()
    app.setOrientation(orient="vertical")  
    app.run()
