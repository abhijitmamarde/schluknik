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
# for date and time stamp
import datetime
import pandas as pd
import csv
import traceback

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
        lat: 50.6394
        lon: 3.057
        zoom: 13
        map_source: MapSource(sys.argv[1], attribution="") if len(sys.argv) > 1 else "osm"

        MapMarkerPopup:
            lat: 50.6394
            lon: 3.057
            popup_size: dp(230), dp(130)

            Bubble:
                BoxLayout:
                    orientation: "horizontal"
                    padding: "5dp"
                    AsyncImage:
                        source: "http://upload.wikimedia.org/wikipedia/commons/9/9d/France-Lille-VieilleBourse-FacadeGrandPlace.jpg"
                        mipmap: True
                    Label:
                        text: "[b]Lille[/b]\\n1 154 861 hab\\n5 759 hab./km2"
                        markup: True
                        halign: "center"
                    Label:
                        text: root.gps_location
                    
""")

###     Screen Declaration     ####    

# create the screen manager
sm = ScreenManager()

class ResultScreen(Screen):

    gps_location = StringProperty()
    gps_status = StringProperty('Click Start to get GPS location updates')

    def build(self):
        self.gps = gps
        try:
            self.gps.configure(on_location=self.on_location,
                               on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        return Builder.load_string(kv)

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        print(self.gps_location)

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    pass

class HangScreen(Screen):

    def addpoop(instance, value):
        """
		Button pressed handler
        """
        global num_hang
        num_hang = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='poop.png')
            instance.grid.add_widget(wimg)

    def ftp_transfer(Screen):
            """
		    Button pressed handler
            """

            filename = "schlukniktable.csv"
            schlukniktable = pd.DataFrame(columns=['timestamp', 'location', 'beer', 'hang'])

            # File FTP transfer
		    # domain name or server ip:
            ftp = FTP('singing-wires.de')
		    # how to encrypt this?
            ftp.login(user='web784', passwd = 'Holz0815')
            ftp.cwd('/html/schluknik')
            
            try:
                gFile = open(filename, "wb")
                ftp.retrbinary("RETR " + filename ,gFile.write)
                ftp.quit()
                gFile.close()
                schlukniktable = pd.read_csv(filename, encoding='utf-8', header=None, sep=';')
            except:
                tb = traceback.format_exc()
            else:
                tb = "No error"
            finally:
                print tb
            

            print(schlukniktable)

            # portfolio
            print(num_beer)
            print(num_hang)
            timestamp = time.strftime('%d%m%y_%H%M%S', time.localtime())
            print(timestamp)
            # apppend data frames
            

            ftp.login(user='web784', passwd = 'Holz0815')
            ftp.cwd('/html/schluknik')
		    # todo: store as .csv file
            with open(filename,"a+") as f:		
                ftp.storlines("STOR " + filename, open(filename, 'r'))
                ftp.quit()

            sm.current = 'result'
    pass 

class BeerScreen(Screen):

    def addbeer(instance, value):
        """
		Button pressed handler
        """
        global num_beer
        num_beer = value
        instance.grid.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source='beerchen.jpg')
            instance.grid.add_widget(wimg)
    pass

    


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
        return sm 

###    entry point      ####
if __name__ == "__main__":
    """
		Entry point for the application
    """
    app = Myapp()
    app.run()
