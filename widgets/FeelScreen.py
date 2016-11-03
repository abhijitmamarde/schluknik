from kivy.uix.screenmanager import ScreenManager, Screen
import numpy as numpy
from setcard import setcard
from ftplib import FTP
import datetime
import csv
import traceback
import io
import json
from pizza import *
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex as rgb
from GraphScreen import GraphScreen
from MapScreen import MapScreen
from kivy.uix.label import Label
from kivy.uix.bubble import Bubble
import numpy as np

#
from graph import *
from mapview import *

from kivy.app import App as app

# for pizza graph
# todos: how to make setcard globally accessible? 
setc = setcard();
# global path to pictures
picpath = 'pics/app/'
# todo: check what is wrong here
global avoid_double_execution
avoid_double_execution = True;

# memory value for previous run
global last_run
last_run = 1

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
                'background_color': rgb('ffffff'),  # back ground color of canvas
                'tick_color': rgb('808080'),  # ticks and grid
                'border_color': rgb('808080')} # border drawn around each graph

        # prepare the hangover forecast
        graphscreen = GraphScreen(name='graph')
        Screen.manager.add_widget(graphscreen)

        Screen.manager.current = 'result'

        # add overview
        graphscreen.grid.add_widget(Label(text = 'total number of todays rating ' + str(Screen.get_total_entries), id = 'get_total_entries', color = [0,0,0,1]))

        # add graph title
        graphscreen.grid.add_widget(Label(text = 'hangover forecast', color = [0,0,0,1]))

        i = Screen.get_timestamp()

        # max forecast of steps
        loop_count = 12

        graph = Graph( xlabel='hours of the day',x_ticks_minor=5,
        x_ticks_major=1, y_ticks_major=2,
        y_grid_label=True, x_grid_label=True, padding=1,
        x_grid=True, y_grid=True, xmin=i[0], xmax=i[loop_count - 1], ymin=0, ymax=10, **graph_theme)

         
        sleepy_plot = SmoothLinePlot(color=[0, 0, 1, 1])
        headache_plot = SmoothLinePlot(color=[1, 0, 0, 1])
        vomit_plot = SmoothLinePlot(color=[0, 1, 0, 1])

        # compute sleepy
        sleepy_plot.points = [(i[x], Screen.sleep_forecast(x, Screen.ids.sleep.value)) for x in range(0, loop_count)] 
        # compute weary
        headache_plot.points = [(i[x], Screen.headache_forecast(x, Screen.ids.headache.value)) for x in range(0, loop_count)] 
        # comute womit  
        vomit_plot.points = [(i[x], Screen.vomit_forecast(x, Screen.ids.vomit.value)) for x in range(0, loop_count)] 
        # add plots to graph
        graph.add_plot(sleepy_plot)
        graph.add_plot(headache_plot)
        graph.add_plot(vomit_plot)

        graphscreen.grid.add_widget(graph)
        
        # calculate alki score from numpy array
        global alki_score
        alki_score = str(round(numpy.mean(alki_mean, axis=0),2))
        setc.hangover_level = alki_score
        graphscreen.ids.alki_score.text = 'hangover level: ' + str(alki_score)

    def sleep_forecast(instance, x, sleep):
        """
        math part for sleep
        """
        # fall time defenitly depends on smoker or not
        # also the n must depend on the number of cigarettes
        m = 1
        y = m*(pow(x-(sleep/3),2)) + (sleep/2)

        # no negative hangover
        if y < 0 or y == 0:
            y = 0

        # not higher than 10
        if y > 10 :
            y = 10

        # average calculator 
        try:
            global alki_mean
            alki_mean = numpy.append(alki_mean,y)
        except:
                tb = traceback.format_exc()
                print (tb)
        
        y = instance.sleep_recover(int(datetime.datetime.now().strftime('%H')) + x,y)
        last_run = round(y,1)
        return y

    def headache_forecast(instance, x, headache):
        """
        math part for headache
        """
        m = 1
        y = m*(x) + headache

        # no negative hangover
        if y < 0 or y == 0:
            y = 0
        # not higher than 10
        if y > 10 :
            y = 10

        y = instance.sleep_recover(int(datetime.datetime.now().strftime('%H')) + x,y)
        last_run = round(y,1)
        return round(y,1)

    def vomit_forecast(instance, x, vomit):
        """
        math part for vomit
        """
        m = -1
        y = m*(x) + vomit

        # no negative hangover
        if y < 0 or y == 0:
            y = 0
        # not higher than 10
        if y > 10 :
            y = 10

        y = instance.sleep_recover(int(datetime.datetime.now().strftime('%H')) + x,y)
        last_run = round(y,1)
        return round(y,1)

    def sleep_recover(instace, time, y):
        """
        compute the slope during night time
        """
        # going to bed value
        start = 23
        global last_run

        if(time < start):
            last_run = y
            return y

        m = -0.5 # slope for recovery during night time
        y = last_run + m
        last_run = y

        # no negative hangover
        if y < 0 or y == 0:
            y = 0
        # not higher than 10
        if y > 10 :
            y = 10

        return round(y,1) 

    def get_timestamp(i):

        str = float(datetime.datetime.now().strftime('%H')) 
        x = [str + i for i in range(12)]

        return x

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
                    
                    # global table to be stored on server
                    new_table = numpy.array([timestamp, Screen.lat, Screen.lon, setc.num_beer, setc.num_wine, setc.num_shot, setc.num_cig, setc.num_tired, setc.num_stress, setc.num_water, setc.num_sleep, setc.num_food, setc.hangover_level], dtype='string')

                except:
                    tb = traceback.format_exc()
                    print (tb)
                # filename of global performance data
                filename = "schlukniktable.csv"

                # combine global and local table
                try:
                    # append old table to new table
                    results = numpy.append(new_table,Screen.global_history)

                    # get total number of entries 
                    Screen.get_total_entries = len(results)/13
                    # prepare graphs
                    Screen.prepareGraphs(Screen)
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
                    Screen.manager.add_widget(map)
                except:
                    tb = traceback.format_exc()
                    print (tb)
                # switch to the result screen 
                Screen.manager.current = 'result'
                avoid_double_execution = False
                return