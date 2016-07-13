#!/usr/bin/env python
"""
		schluknik 2016
		run with python 2.7.6
"""

################################################################################################

####    Author Information      ####

__author__ = "Elias Kardel"
__copyright__ = "Copyright 2016t"
__credits__ = ["Elias Kardel"]
__license__ = "GPL"
__maintainer__ = "Elias Kardel"
__email__ = "elias.kardel@u-blox.com"
__status__ = "development"

################################################################################################

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
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.bubble import Bubble
from kivy.garden.mapview import *

# for date and time stamp
import datetime
import numpy as numpy
import csv
import traceback
import io

################################################################################################

###     kv integration     ###
Builder.load_string("""
#:import sys sys
#:import MapSource mapview.MapSource
#:import MapMarkerPopup kivy.garden.mapview.MapMarkerPopup
    
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
    grid1: Grid1
    grid2: Grid2
    grid3: Grid3
    MyBoxLayout:
        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'top'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: .3, .3
                Button:
                    text: 'Settings'
                    on_press: root.manager.current = 'setting'
        GridLayout:
            cols: 2
            rows: 1
            HeaderImage:
                source: 'icon.png'
            HeaderLabel:
                text: 'Lets face it! You have been a schluknik again!'

        GridLayout:
            cols: 2
            rows: 1
            Slider:
                id: slider_id1
                min: 0
                step: 0.5
                max: 10
                on_value: root.addbeer(slider_id1.value)
            Label:
                text:  str(round(slider_id1.value, 1)) + ' x Beer'
                color: 0,0,0,1
        GridLayout:
            id: Grid1
            cols: 10
            rows: 1
        GridLayout:
            cols: 2
            rows: 1
            Slider:
                id: slider_id2
                min: 0
                step: 0.5
                max: 10
                on_value: root.addwine(slider_id2.value)
            Label:
                text:  str(round(slider_id2.value, 1)) + ' x Wine'
                color: 0,0,0,1
        GridLayout:
            id: Grid2
            cols: 10
            rows: 1

        GridLayout:
            cols: 2
            rows: 1
            Slider:
                id: slider_id3
                min: 0
                step: 1
                max: 10
                on_value: root.addshot(slider_id3.value)
            Label:
                text:  str(round(slider_id3.value, 1)) + ' x Shot'
                color: 0,0,0,1
        GridLayout:
            id: Grid3
            cols: 10
            rows: 1

        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'bottom'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: .3, .3
                Button:
                    text: 'OK'
                    on_press: root.manager.current = 'hang'
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

<MapScreen>:
    MapView:
        id: map
        lat: app.lat
        lon: app.lon
        zoom: 13
        map_source: MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"

<SettingsScreen>:
    MyBoxLayout: 
        AnchorLayout:
            anchor_x: 'right'
            anchor_y: 'bottom'
            BoxLayout:
                orientation: 'horizontal'
                size_hint: .3, .3
                Button:
                    text: 'Back'
                    on_press: root.manager.current = 'beer'

<ResultScreen>:
    Button: 
        text: 'Result'
        on_press: root.manager.current = 'map'
""")

###     globals     ####   
# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

###     Screen Declarations     ####

################################################################################################

class MapScreen(Screen):
    """
    Shows map of all the schlukniks
    """
################################################################################################

class ResultScreen(Screen):
    """
    Show overall hangover result
    """
################################################################################################

class SettingsScreen(Screen):
    """
    Set personal settings
    """
    # todo: add boy or girl 
    # todo: add smoker 
    # todo: add body size 
    # todo: add body weight 



################################################################################################
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
                # todo: extend
                # timestamp | latitude | longitude | number of beer | number of hang 
                try:
                    new_table = numpy.array([timestamp,app.lat,app.lon,num_beer,num_hang  ], dtype='string')
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
                    results = results.reshape((len(results)/5,5))
                    # store data as a local csv file 
                    numpy.savetxt(filename, results, delimiter=';', fmt=('%s', '%s', '%s', '%s','%s'))
                    
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

                # finished ftp connection now fill
                lat = numpy.array(results)[:,1].tolist()
                lon = numpy.array(results)[:,2].tolist()
                
                # create result screen widget
                map = MapScreen(name='map')
                try:
                    # todo: can this be more pythonic?
                    i = 0
                    # set marker for every entry in table
                    for item in lat:
                        # change this to pop up marker 
                        m = MapMarker(lon=float(lon[i]), lat=float(lat[i]))
                        map.ids.map.add_marker(m)
                        i = i + 1
                    app.sm.add_widget(map)
                except:
                    tb = traceback.format_exc()
                    print (tb)
                # switch to the result screen 
                Screen.manager.current = 'result'
                avoid_double_execution = False
                return

################################################################################################

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
        instance.grid1.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='beerchen.jpg')
            instance.grid1.add_widget(wimg)

    def addwine(instance, value):
        """
        Adding the beer picture
        """
        global num_wine
        num_wine = value
        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='wine.png')
            instance.grid2.add_widget(wimg)

    def addshot(instance, value):
        """
        Adding the beer picture
        """
        global num_wine
        num_wine = value
        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='shot.jpg')
            instance.grid3.add_widget(wimg)

################################################################################################

###     Body        ###
class Myapp(App):
    """
    Main class
    """

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
        # set bg color to white
        notification.notify('test tiltle','scanning started')
        Window.clearcolor = (1, 1, 1, 0)
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

        # adding all the sub screens to the screen handler
        # create the screen manager
        self.sm = ScreenManager()
        self.sm.add_widget(BeerScreen(name='beer'))
        self.sm.add_widget(HangScreen(name='hang'))
        self.sm.add_widget(SettingsScreen(name='setting'))
        self.sm.add_widget(ResultScreen(name='result'))
        return self.sm

################################################################################################

###    entry point      ####
if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
