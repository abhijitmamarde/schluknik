import kivy
import random

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from ftplib import FTP

red = [1,0,0,1]
green = [0,1,0,1]
blue =  [0,0,1,1]
purple = [1,0,1,1]

########################################################################
class HBoxLayoutExample(App):
    """
    Horizontally oriented BoxLayout example class
    """

    #----------------------------------------------------------------------
    def build(self):
        """
        Horizontal BoxLayout example
        """
        layout = BoxLayout(padding=10)
        colors = [red, green, blue, purple]

        for i in range(5):
            btn = Button(text="Button #%s" % (i+1),
                         background_color=random.choice(colors)
                         )

            layout.add_widget(btn)
        return layout

########################################################################
class VBoxLayoutExample(App):
    """
    Vertical oriented BoxLayout example class
    """

    #----------------------------------------------------------------------
    def setOrientation(self, orient):
        """"""
        self.orient = orient

	
    def callback(instance, event):
	#domain name or server ip:
	ftp = FTP('singing-wires.de') 
	ftp.login(user='web784', passwd = 'Holz0815')
	ftp.cwd('/html/schluknik')
	filename = event.text + ".txt"
	with open(filename,"a+") as f:		
		ftp.storlines("STOR " + filename, open(filename, 'r'))
		ftp.quit()
		print('sucessfully created file'+ filename)
	

    #----------------------------------------------------------------------
    def build(self):
        """"""
        layout = BoxLayout(padding=10, orientation=self.orient)

        for i in range(5):
            btn = Button(text="Button%s" % (i+1) )
	    btn.bind(on_press=self.callback)
            layout.add_widget(btn)
        return layout

#----------------------------------------------------------------------
if __name__ == "__main__":
    #app = HBoxLayoutExample()
    app = VBoxLayoutExample()
    app.setOrientation(orient="vertical")
    app.run()
