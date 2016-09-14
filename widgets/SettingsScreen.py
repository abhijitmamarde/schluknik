from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.settings import Settings
from  kivy.uix.settings import InterfaceWithNoMenu
from kivy.uix.label import Label

#class KognitivoSettingsInterface(InterfaceWithNoMenu):  
#    pass

#class KognitivoSettings(Settings):  
#    def __init__(self, **kwargs):
#        super(KognitivoSettings, self).__init__(**kwargs)
#        self.register_type('title', KognitivoSettingTitle)


#class KognitivoSettingTitle(Label):  
#    title = Label.text

#def add_kivy_panel(self):
#        pass

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