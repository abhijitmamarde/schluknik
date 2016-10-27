from kivy.uix.screenmanager import ScreenManager, Screen
from setcard import setcard
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.window import Window

setc = setcard();
# global path to pictures 
picpath = 'pics/app/'

class DrinkScreen(Screen):
    """
    Evaluating your performance
    """

    ## animation
    #def animate(self, id):
    #    '''
    #    Animate the arrival of the bullets
    #    '''
    #    animation = Animation(right=1070.0, opacity=1, d=3, t='out_elastic')
    #    animation.cancel(id)
    #    animation.start(id)

    # set zero global variables
    # todo: is there a better OOP approach for this??
    def addbeer(instance, value):
        """
		Adding the beer picture
        """
        setc.num_beer = value

        instance.grid1.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'beer_round.png', mipmap= True)
            instance.grid1.add_widget(wimg)
        #DrinkScreen.animate(instance, instance.grid1)

    def addwine(instance, value):
        """
        Adding the wine picture
        """
        setc.num_wine = value

        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'wine.png', mipmap= True)
            instance.grid2.add_widget(wimg)
        #DrinkScreen.animate(instance, instance.grid2)

    def addshot(instance, value):
        """
        Adding the shot picture
        """
        setc.num_shot = value

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + 'shot.png', mipmap= True)
            instance.grid3.add_widget(wimg)
        #DrinkScreen.animate(instance, instance.grid3)
