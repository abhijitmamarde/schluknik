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
#from kivy.garden.mapview import *

from mapview import *

# for date and time stamp
import datetime
import numpy as numpy
import csv
import traceback
import io

import math_engine

# for graph 
from math import sin
#from kivy.garden.graph import *
from graph import *

################################################################################################

###    KV Integration    ####

################################################################################################

# load style file
Builder.load_file('style.kv')

###     globals     ####   
# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

################################################################################################

###     Screen Classes     ####

################################################################################################

class GraphScreen(Screen):
    """
    Shows map of all the schlukniks
    """
    def __init__(self, **kwargs):
        super(GraphScreen, self).__init__(**kwargs)

        graph = Graph(background_color = [0,0,0,1], xlabel='X', ylabel='Y', x_ticks_minor=5,
        x_ticks_major=25, y_ticks_major=1,
        y_grid_label=True, x_grid_label=True, padding=5,
        x_grid=True, y_grid=True, xmin=-0, xmax=100, ymin=-1, ymax=1)
        plot = MeshLinePlot(color=[0, 0, 1, 1])
        plot.points = [(x, sin(x / 10.)) for x in range(0, 101)]
        graph.add_plot(plot)
        self.grid.add_widget(graph)

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

class HealScreen(Screen):
    """
    positive counter measures
    """

    global num_water
    num_water = 0.0
    global num_sleep
    num_sleep = 0.0
    global num_food
    num_food = 0.0

    def addwater(instance, value):
        """
        adding the glass of water count
        """
        global num_water
        num_water = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='water.png')
            instance.grid.add_widget(wimg)

    def addsleep(instance, value):
        """
        adding the sleep read
        """
        global num_sleep
        num_sleep = value
        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='sleep.jpg')
            instance.grid2.add_widget(wimg)

    def addfood(instance, value):
        """
		adding what was eaten before
        """
        global num_food
        num_food = value

        switcher = {
        0: "nothing",
        1: "almost nothing",
        2: "snack",
        3: "small lunch",
        4: "lunch",
        5: "medium",
        6: "more than usually",
        7: "proper drinking preparation : )",
        8: "too much : ( !",
        9: "way too much!!",
        10: "lethal!!!"
        }

        switcher_pic = {
        0: "banana.jpg",
        1: "banana.jpg",
        2: "banana.jpg",
        3: "sushi.png",
        4: "sushi.png",
        5: "sushi.png",
        6: "burger.png",
        7: "burger.png",
        8: "burger.png",
        9: "skull.png",
        10: "skull.png"
        }

        instance.foodranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=pic)
            instance.grid3.add_widget(wimg)


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
                # timestamp | latitude | longitude | number of beer | number of wine | number of shots |  number of cigarettes | XX | XX | number of water | number of sleep | number of food
                try:
                    new_table = numpy.array([timestamp,app.lat,app.lon, num_beer,num_wine,num_shot,num_cig,num_water,num_sleep,num_food], dtype='string')
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

                # finished ftp connection now fill result computer
                lat = numpy.array(results)[:,1].tolist()
                lon = numpy.array(results)[:,2].tolist()

                info_box_beer = numpy.array(results)[:,3].tolist()
                
                # create result screen widget
                map = MapScreen(name='map')
                try:
                    # todo: can this be more pythonic?BeerScreen
                    i = 0
                    # set marker for every entry in table
                    for item in lat:
                        # change this to pop up marker
                        a = Bubble(size= (400, 400))
                        a.add_widget(Label(text=str(info_box_beer[i])))
                        m = MapMarkerPopup(lon=float(lon[i]), lat=float(lat[i]), placeholder= a)
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

class DestroyScreen(Screen):
    """
    Evaluating the non-drinkable influences
    """
    global num_cig
    num_cig = 0.0

    def addcigarette(instance, value):
        """
		adding the cigarette picture
        """
        global num_cig
        num_cig = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='cigarette.png')
            instance.grid.add_widget(wimg)

    # todo: add stress
    # todo: add cocktail

    
################################################################################################

class DrinkScreen(Screen):
    """
    Evaluating your performance
    """
    # set zero global variables
    # todo: is there a better OOP approach for this??
    global num_beer
    num_beer = 0.0

    global num_wine
    num_wine = 0.0

    global num_shot
    num_wine = 0.0

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
        global num_shot
        num_shot = value

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='shot.jpg')
            instance.grid3.add_widget(wimg)

################################################################################################

###    Body     ####

################################################################################################

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
        
        
        self.sm.add_widget(DrinkScreen(name='drink'))
        self.sm.add_widget(DestroyScreen(name='destroy'))
        self.sm.add_widget(HealScreen(name='heal'))
        self.sm.add_widget(SettingsScreen(name='setting'))
        self.sm.add_widget(ResultScreen(name='result'))
        self.sm.add_widget(GraphScreen(name='graph'))
        

        return self.sm

################################################################################################

###    Entry point     ####

################################################################################################

if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
