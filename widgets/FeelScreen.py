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
        Screen.manager.add_widget(graphscreen)

        
        Screen.manager.current = 'result'
        return
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
        return 
    
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