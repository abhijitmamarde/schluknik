from kivy.uix.screenmanager import ScreenManager, Screen
from setcard import setcard
from kivy.uix.image import Image

setc = setcard();
# global path to pictures 
picpath = 'pics/app/'

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
