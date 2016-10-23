from kivy.uix.screenmanager import ScreenManager, Screen
from setcard import setcard
from kivy.uix.image import Image

setc = setcard();
# global path to pictures
picpath = 'pics/app/'

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
            wimg = Image(source=picpath + 'cigarette.png', mipmap= True)
            instance.grid.add_widget(wimg)

    def addtired(instance, value):
        """
	    adding Energy
        """
        setc.num_tired = value

        switcher = {
        0: "none",
        1: "sloth",
        2: "powerless",
        3: "weary",
        4: "tired",
        5: "normal",
        6: "sporty",
        7: "vital",
        8: "energetic",
        9: "superman",
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

        instance.tiredranking.text = switcher.get(value, "Tired?")

        pic = switcher_pic.get(value, "banana.png")

        instance.grid2.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic, mipmap= True)
            instance.grid2.add_widget(wimg)

    def addstress(instance, value):
        """
		adding Emotion
        """
        setc.num_stress = value

        switcher = {
        0: "none",
        1: "radicalised",
        2: "depressed",
        3: "agressive",
        4: "stressed",
        5: "normal",
        6: "happy",
        7: "excited",
        8: "8!",
        9: "9!!",
        10: "party!!!"
        }

        switcher_pic = {
        0: "depressed.png",
        1: "depressed.png",
        2: "sad.png",
        3: "agressive.png",
        4: "agressive.png",
        5: "normal.png",
        6: "normal.png",
        7: "normal.png",
        8: "normal.png",
        9: "skull.png",
        10: "skull.png"
        }

        instance.stressranking.text = switcher.get(value, "Food??")

        pic = switcher_pic.get(value, "banana.jpg")

        instance.grid3.clear_widgets()
        for x in range(0, int(value)):
            wimg = Image(source=picpath + pic, mipmap= True)
            instance.grid3.add_widget(wimg)