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
from geartick import *

import os.path

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
import json
from setcard import setcard

# for graph 
from graph import *
from kivy.utils import get_color_from_hex as rgb

################################################################################################

###    KV Integration    ####

################################################################################################

# load style file
Builder.load_file('style.kv')

################################################################################################
setc = setcard();

###     globals     ####   
# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

# global path to pictures 

picpath = 'pics/app/'



################################################################################################

###     Screen Classes     ####

################################################################################################

class GraphScreen(Screen):
    """
    Shows map of all the schlukniks
    """
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
    def storetojson(Screen):
        """
        store settings as json
        """
        # create dictionary
        data = {}

        data['smoker'] = setc.smoker
        data['boy'] = setc.boy
        data['girl'] = setc.girl
        data['age']  = setc.age
        data['height'] = setc.height 
        data['weight'] = setc.weight
        with open('data.json', 'w') as fp:
            json.dump(data, fp)
        Screen.manager.current = 'drink'
        return

    # setter functions for settings variables
    def age(instance, value):
            setc.age = value

    def high(instance, value):
            setc.height = value

    def weight(instance, value):
            setc.weight = value

    def girl(instance, value):
            if(value == 'down'):
                setc.girl = True
                setc.boy = False

    def boy(instance, value):
            if(value == 'down'):
                setc.boy = True
                setc.girl = False

    def smoker(instance, value):
        if(value == 'down'):
            setc.smoker = True
        else:
            setc.smoker = False

################################################################################################

class FeelScreen(Screen):
    """
    positive counter measures
    """
    # global alki score
    global alki_mean
    alki_mean = numpy.array([0])

    def prepareGraphs(Screen,event):
        """
        prepare graphical evaluation
        """
        # layout of the plot
        graph_theme = {
                'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
                'background_color': rgb('f8f8f2'),  # back ground color of canvas
                'tick_color': rgb('808080'),  # ticks and grid
                'border_color': rgb('808080')} # border drawn around each graph

        # prepare the hangover forecast
        graphscreen = GraphScreen(name='graph')
        app.sm.add_widget(graphscreen)

        # add graph title
        graphscreen.grid.add_widget(Label(text = 'hangover forecast', color = [0,0,0,1]))

        graph = Graph( xlabel='time', ylabel='today', x_ticks_minor=5,
        x_ticks_major=1, y_ticks_major=2,
        y_grid_label=True, x_grid_label=True, padding=1,
        x_grid=True, y_grid=True, xmin=-0, xmax=12, ymin=0, ymax=10, **graph_theme)

        plot = SmoothLinePlot(color=[0, 0, 1, 1])
        ## add points to plot
        plot.points = [(x, Screen.hang_forecast(x)) for x in range(0, 12)]
        graph.add_plot(plot)
        graphscreen.grid.add_widget(graph)
        
         # add graph title
        graphscreen.grid.add_widget(Label(text = 'hangover history', color = [0,0,0,1]))

        # prepare graph for personal history
        history = Graph( xlabel='time', ylabel='history', x_ticks_minor=5,
        x_ticks_major=1, y_ticks_major=2,
        y_grid_label=True, x_grid_label=True, padding=1,
        x_grid=True, y_grid=True, xmin=-0, xmax=12, ymin=0, ymax=10, **graph_theme)

        plot = SmoothLinePlot(color=[0, 1, 1, 1])
        ## add points to plot
        plot.points = [(x, Screen.hang_forecast(x)) for x in range(0, 12)]
        history.add_plot(plot)
 
        graphscreen.grid.add_widget(history)
        
        # calculate alki score from numpy array
        global alki_score
        alki_score = str(round(numpy.mean(alki_mean, axis=0),2))
        setc.hangover_level = alki_score
        graphscreen.ids.alki_score.text = 'hangover level: ' + str(alki_score)

    def hang_forecast(instance, x):
        """
        math part
        """
        # fall time defenitly depends on smoker or not
        # also the n must depend on the number of cigarettes
        m = -0.7
        y = m*x + setc.num_beer

        # no negative hangover
        if y < 0:
            y = 0

        # average calculator 
        try:
            global alki_mean
            alki_mean = numpy.append(alki_mean,y)
        except:
                tb = traceback.format_exc()
                print (tb)
        return y


    def addsleepy(instance, value):
        """
		adding what was eaten before
        """
        setc.num_food = value

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

        instance.sleepranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.sleepy_grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic)
            instance.sleepy_grid.add_widget(wimg)


    def addheadache(instance, value):
        """
		adding what was eaten before
        """
        setc.num_food = value

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

        instance.headacheranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.headache_grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic)
            instance.headache_grid.add_widget(wimg)


    def addvomit(instance, value):
        """
		adding what was eaten before
        """
        setc.num_food = value

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

        instance.vomitranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.vomit_grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic)
            instance.vomit_grid.add_widget(wimg)

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
                # table format
                # 13 pcs
                # |timestamp | latitude | longitude | beer | wine | shots | cigarettes | tired | stressed | water | sleep | food | hang_level
                try:
                    Screen.prepareGraphs(Screen)
                    # global table to be stored on server
                    new_table = numpy.array([timestamp, app.lat, app.lon, setc.num_beer, setc.num_wine, setc.num_shot, setc.num_cig, setc.num_tired, setc.num_stress, setc.num_water, setc.num_sleep, setc.num_food, setc.hangover_level], dtype='string')
                except:
                    tb = traceback.format_exc()
                    print (tb)
                # filename of global performance data
                filename = "schlukniktable.csv"

                # combine global and local table
                try:
                    # append old table to new table
                    results = numpy.append(new_table,app.global_history)
                    results = results.reshape((len(results)/13,13))
                    # store data as a local csv file 
                    numpy.savetxt(filename, results, delimiter=';', fmt=('%s', '%s', '%s', '%s','%s','%s', '%s', '%s', '%s','%s', '%s','%s','%s'))
                    
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
                info_box_beer = numpy.array(results)[:,12].tolist()
                
                # create result screen widget
                map = MapScreen(name='map')
                try:
                    # todo: can this be more pythonic?BeerScreen
                    i = 0
                    # set marker for every entry in table
                    for item in lat:
                        # change this to pop up marker
                        a = Bubble(size= (400, 400))
                        a.add_widget(Label(text='hangover level ' + str(info_box_beer[i])))
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

class HealScreen(Screen):
    """
    positive counter measures
    """
    # global alki score
    global alki_mean
    alki_mean = numpy.array([0])

    def prepareGraphs(Screen,event):
        """
        prepare graphical evaluation
        """
        # layout of the plot
        graph_theme = {
                'label_options': {
                'color': rgb('444444'),  # color of tick labels and titles
                'bold': True},
                'background_color': rgb('f8f8f2'),  # back ground color of canvas
                'tick_color': rgb('808080'),  # ticks and grid
                'border_color': rgb('808080')} # border drawn around each graph

        # prepare the hangover forecast
        graphscreen = GraphScreen(name='graph')
        app.sm.add_widget(graphscreen)
        graph = Graph( xlabel='time', ylabel='hangover', x_ticks_minor=5,
        x_ticks_major=1, y_ticks_major=2,
        y_grid_label=True, x_grid_label=True, padding=1,
        x_grid=True, y_grid=True, xmin=-0, xmax=12, ymin=0, ymax=10, **graph_theme)
        plot = SmoothLinePlot(color=[0, 0, 1, 1])

        ## add points to plot
        plot.points = [(x, Screen.hang_forecast(x)) for x in range(0, 12)]
        graph.add_plot(plot)
        graphscreen.grid.add_widget(graph)
        
        # calculate alki score from numpy array
        global alki_score
        alki_score = str(round(numpy.mean(alki_mean, axis=0),2))
        setc.hangover_level = alki_score
        graphscreen.ids.alki_score.text = 'hangover level: ' + str(alki_score)

    def hang_forecast(instance, x):
        """
        math part
        """
        # fall time defenitly depends on smoker or not
        # also the n must depend on the number of cigarettes
        m = -0.7
        y = m*x + setc.num_beer

        # no negative hangover
        if y < 0:
            y = 0

        # average calculator 
        try:
            global alki_mean
            alki_mean = numpy.append(alki_mean,y)
        except:
                tb = traceback.format_exc()
                print (tb)
        return y

    def addwater(instance, value):
        """
        adding the glass of water count
        """
        setc.num_water = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source= picpath + 'water.png')
            instance.grid.add_widget(wimg)

    def addsleep(instance, value):
        """
        adding the sleep read
        """
        setc.num_sleep = value
        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source= picpath + 'sleep.jpg')
            instance.grid2.add_widget(wimg)

    def addfood(instance, value):
        """
		adding what was eaten before
        """
        setc.num_food = value

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
            wimg = Image(source=picpath + pic)
            instance.grid3.add_widget(wimg)

        
    # todo: add computation for the hangover forecast
    def CompHangoverForecast(Screen):

        # switch to feel screen to get correction
        feelscreen = FeelScreen(name='feel')
       
        # compute sleepy avg and add to slider
        sleepy_avg = Screen.CompSleepy(Screen)
        feelscreen.ids.sleep.value = sleepy_avg

        # compute weary avg

        # compute vomit avg

        # switch over to feelscreen
        app.sm.add_widget(feelscreen)
        Screen.manager.current = 'feel'


    # todo compute sleepy
    def CompSleepy(Screen, event):
        '''
        The rating for sleepyness depends on the hours slept and on the energy one had before going out
        '''
        # number of sleep hours 
        max_sleep_time = 12
        # calculate avg with weighting factors
        sleepy_avg = 0.8*(max_sleep_time - setc.num_sleep) - 0.35*(setc.num_tired) - 0.1*(setc.num_stress)
        # value shouldnt be higher than 10 and not lower than 0
        if(sleepy_avg > 10):
            sleepy_avg = 10
        if(sleepy_avg < 0):
            sleepy_avg = 0

        return sleepy_avg

    # todo compute weary 
    def CompWeary(Screen,event):
        return

    # todo compute vomit
    def CompVomit(Screen,event):
        return

################################################################################################

class DestroyScreen(Screen):
    """
    Evaluating the non-drinkable influences
    """
    def addcigarette(instance, value):
        """
		adding the cigarette picture
        """
        setc.num_cig = value

        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'cigarette.png')
            instance.grid.add_widget(wimg)

    def addtired(instance, value):
        """
	    adding tiredness
        """
        setc.num_tired = value

        switcher = {
        0: "stress",
        1: "stress",
        2: "stress",
        3: "stress",
        4: "stress",
        5: "stress",
        6: "stress",
        7: "stress",
        8: "stress",
        9: "stress",
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

        instance.tiredranking.text = switcher.get(value, "Tired?")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic)
            instance.grid2.add_widget(wimg)

    def addstress(instance, value):
        """
		adding stress
        """
        setc.num_stress = value

        switcher = {
        0: "stress",
        1: "stress",
        2: "stress",
        3: "stress",
        4: "stress",
        5: "stress",
        6: "stress",
        7: "stress",
        8: "stress",
        9: "stress",
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

        instance.stressranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic)
            instance.grid3.add_widget(wimg)

    
################################################################################################

class DrinkScreen(Screen):
    """
    Evaluating your performance
    """
    # set zero global variables
    # todo: is there a better OOP approach for this??

    def addbeer(instance, value):
        """
		Adding the beer picture
        """
        setc.num_beer = value

        instance.grid1.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'beer.png')
            instance.grid1.add_widget(wimg)

    def addwine(instance, value):
        """
        Adding the wine picture
        """
        setc.num_wine = value

        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'wine.png')
            instance.grid2.add_widget(wimg)

    def addshot(instance, value):
        """
        Adding the shot picture
        """
        setc.num_shot = value

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'shot.jpg')
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
            self.alki_score = ""

        # create the screen manager
        self.sm = ScreenManager()

        try: 
            # check the seetings config
            with open('data.json', 'r') as fp:
                data = json.load(fp)
                self.smoker = data['smoker']  
                self.boy = data['boy'] 
                self.girl = data['girl'] 
                self.age = str(data['age'])  
                self.height = data['height'] 
                self.weight = data['weight']

                self.sm.add_widget(DrinkScreen(name='drink'))
                setting = SettingsScreen(name='setting')
                setting.ids.gear_tick.value = float(data['age'])
                self.sm.add_widget(setting)

        except:
               setting = SettingsScreen(name='setting')
               self.sm.add_widget(setting)
               self.sm.add_widget(DrinkScreen(name='drink'))
                
        # adding all the sub screens to the screen handler
        self.sm.add_widget(DestroyScreen(name='destroy'))
        self.sm.add_widget(HealScreen(name='heal'))
        self.sm.add_widget(ResultScreen(name='result'))

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

################################################################################################

###    Entry point     ####

################################################################################################

if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
