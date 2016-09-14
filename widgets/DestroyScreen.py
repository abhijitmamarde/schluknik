from kivy.uix.screenmanager import ScreenManager, Screen

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