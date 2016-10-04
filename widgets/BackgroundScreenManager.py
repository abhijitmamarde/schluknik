from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image

class BackgroundScreenManager(ScreenManager):
    """description of class"""
    background_image = ObjectProperty(
    Image(source='pics/app/back_.png')
    )




