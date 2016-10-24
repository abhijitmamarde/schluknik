from kivy.uix.screenmanager import ScreenManager, Screen
import numpy as numpy
from setcard import setcard
from kivy.uix.image import Image
from FeelScreen import FeelScreen
from pizza import *
from kivy.app import App
setc = setcard();
# global path to pictures
picpath = 'pics/app/'
import BackgroundScreenManager

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
            wimg = Image(source= picpath + 'water.png', mipmap= True)
            instance.grid.add_widget(wimg)

    def addsleep(instance, value):
        """
        adding the sleep read
        """
        setc.num_sleep = value
        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source= picpath + 'sleep.png', mipmap= True)
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
        8: "too much",
        9: "way too much!",
        10: "party!!"
        }

        switcher_pic = {
        0: "banana.png",
        1: "banana.png",
        2: "banana.png",
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

        pic = switcher_pic.get(value, "banana.png")

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic, mipmap= True)
            instance.grid3.add_widget(wimg)

        
    # todo: add computation for the hangover forecast
    def CompHangoverForecast(Screen):

        # switch to feel screen to get correction
        feelscreen = FeelScreen(name='feel')
       
        # compute sleepy avg and add to slider
        sleepy_avg = Screen.CompSleepy(Screen)
        feelscreen.ids.sleep.value = sleepy_avg
        
        # compute weary avg
        weary_avg = Screen.CompWeary(Screen, sleepy_avg)
        feelscreen.ids.headache.value = weary_avg

        # compute vomit avg
        vomit_avg = sleepy_avg

        # prepare pie chart
        G = sleepy_avg + weary_avg + vomit_avg
        setc.sleepy_avg_pie = (100/G) * sleepy_avg
        setc.headache_avg_pie = (100/G) * weary_avg
        setc.vomit_avg_pie = (100/G) * vomit_avg

        # switch over to feelscreen
        Screen.add_widget(feelscreen)
        Screen.manager.add_widget(feelscreen)
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
    def CompWeary(Screen,event, sleepy_avg):
        # weary is caused by sleepyness + alk; can only be improved by food 
        weary_avg = 0.3*setc.num_beer + 0.2*setc.num_cig +  0.4*setc.num_shot + 0.2*sleepy_avg - 0.5*setc.num_food - 0.5*setc.num_tired
        # value shouldnt be higher than 10 and not lower than 0
        if(weary_avg > 10):
            weary_avg = 10
        if(weary_avg < 0):
            weary_avg = 0
        return weary_avg

    # todo compute vomit
    def CompVomit(Screen,event):
        return
