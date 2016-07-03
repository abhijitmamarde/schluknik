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
# for gps access 
from plyer import gps
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from plyer import notification

# for date and time stamp
import datetime
import numpy as numpy
import csv
import traceback
import io

###     kv integration     ###
Builder.load_string("""
#:import sys sys
#:import MapSource mapview.MapSource

    
<FTPButton@Button>:
    color: 1,1,1,1
    font_size: 32
 
<MyBoxLayout@BoxLayout>:
    orientation: 'vertical'
    padding: 60,60,30,30
    spacing: 5
               
<HeaderLabel@Label>:
    color: 0,0,0,1
    text_size: root.width, None
    size: self.texture_size
    font_size: 35
    font_name: 'Roboto'
    halign: 'left'
    valign: 'middle'

<HeaderImage@Image>
    scale: 6.0

<BeerScreen>:
    grid: Grid
    MyBoxLayout:
        GridLayout:
            cols: 2
            rows: 1
            HeaderImage:
                source: 'icon.png'
            HeaderLabel:
                text: 'Lets face it! You have been a schluknik again! Remember how many beer?'
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
        GridLayout:
            cols: 2
            rows: 1
            HeaderImage:
                source: 'icon.png'
            HeaderLabel:
                text: 'Yuck...And how do you feel today?'
        Slider:
            id: slider_id
            min: 0
            step: 0.01
            max: 10
            on_touch_up: root.ftp_transfer()
            on_value: root.addpoop(slider_id.value)
        Label:
            text: str(round(slider_id.value, 0))
            color: 0,0,0,1
        GridLayout:
            id: Grid
            cols: 10
            rows: 1
<ResultScreen>:
    MapView:
        lat: root.lati
        lon: root.longi
        zoom: 13
        map_source: MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"

        MapMarkerPopup:
            lat: root.lati
            lon: root.longi
            popup_size: dp(230), dp(130)

            Bubble:
                BoxLayout:
                    orientation: "horizontal"
                    padding: "5dp"
                    Label:
                        text: app.global_location

                    
""")

###     globals     ####   
# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

###     Screen Declaration     ####    


class ResultScreen(Screen):
    """
    Shows map of all the schlukniks
    """

    #  gps default values for Berlin
    lati = 52.5192
    longi = 13.4061



class HangScreen(Screen):
    """
    Evaluating the hangover
    """
    def addpoop(instance, value):
        """
		adding the shitty picture
        """
        global num_hang
        num_hang = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='poop.png')
            instance.grid.add_widget(wimg)

    def ftp_transfer(Screen):
            """
		    accessing the global performance data
            """
            # todo: what is going wrong here?
            global avoid_double_execution
            if(bool(avoid_double_execution)):
                # get timestamp
                timestamp =  datetime.datetime.now()

                # portfolio pandas datastructure
                # timestamp | latitude | longitude | number of beer | number of hang 
                try:
                    new_table = numpy.array([timestamp,str(ResultScreen.lati),str(ResultScreen.longi),num_beer,num_hang  ], dtype='string')
                except:
                    tb = traceback.format_exc()
                    print (tb)
                
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
                    old_table = numpy.genfromtxt(filename, delimiter=';', dtype='string')
                except:
                    tb = traceback.format_exc()
                    print (tb)
                
                # combine global and local table
                try:
                    # append old table to new table
                    results = numpy.append(new_table,old_table)
                    # store data as a local csv file 
                    numpy.savetxt(filename, results.reshape((len(results)/5,5)), delimiter=';', fmt=('%s', '%s', '%s', '%s','%s'))
                except:
                    tb = traceback.format_exc()
                    print (tb)
                # up load to ftp
                # File FTP transfer
		        # domain name or server ip:
                ftp = FTP('singing-wires.de')
		        # how to encrypt this?
                ftp.login(user='web784', passwd = 'Holz0815')
                ftp.cwd('/html/schluknik')

		        # todo: store as .csv file
                with open(filename,"a+") as f:		
                    ftp.storlines("STOR " + filename, open(filename, 'r'))
                    ftp.quit()
                # goto result screen
                Screen.manager.current = 'result'
                avoid_double_execution = False

    pass 
class BeerScreen(Screen):
    """
    Evaluating your performance
    """
    def addbeer(instance, value):
        """
		Adding the beer picture
        """
        global num_beer
        num_beer = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='beerchen.jpg')
            instance.grid.add_widget(wimg)
    pass



###     Body        ###
class Myapp(App):
    global_location = StringProperty()
    lat = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')
    """
    Main class
    """
    @mainthread
    def on_location(self, **kwargs):
        self.global_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def build(self):
        """
		Layout builder of main window
        """
        # set bg color to white
        notification.notify('test tiltle','scanning started')
        Window.clearcolor = (1, 1, 1, 0)
        self.gps = gps
        try:
            self.gps.configure(on_location=self.on_location,
                               on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'
        self.gps.start()
        # adding all the sub screens to the screen handler
        # create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(BeerScreen(name='beer'))
        self.sm.add_widget(ResultScreen(name='result'))
        self.sm.add_widget(HangScreen(name='hang'))
        return self.sm

###    entry point      ####
if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
