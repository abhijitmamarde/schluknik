########################################################################
#			schluknik 2016
#			run with python 2.7.6
########################################################################

import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from ftplib import FTP
from kivy.core.window import Window


########################################################################
class VBoxLayoutExample(App):
    """
    Vertical oriented BoxLayout example class
    """

    #----------------------------------------------------------------------
    def setOrientation(self, orient):
        """"""
        self.orient = orient

    #--- Callback when button is pressed
    def callback(instance, event):
	#--- File FTP transfer
	#domain name or server ip:
	ftp = FTP('singing-wires.de') 
	# how to encrypt this?
	ftp.login(user='web784', passwd = 'Holz0815')
	ftp.cwd('/html/schluknik')
	filename = event.text + ".txt"
	# todo: store as .csv file
	with open(filename,"a+") as f:		
		ftp.storlines("STOR " + filename, open(filename, 'r'))
		ftp.quit()
		print('sucessfully created file'+ filename)
	

    #--- Introductional screen 
    def build(self):
        """"""
	
        layout = BoxLayout(padding=10, orientation=self.orient)
	
	l = Label(text='Where have you been last night?')
        l.bind(texture_size=l.setter('size'))

	layout.add_widget(l)
        for i in range(5):
            btn = Button(text="Button%s" % (i+1) )
	    btn.bind(on_press=self.callback)
            layout.add_widget(btn)
        return layout

#--- Entry Point
if __name__ == "__main__":
    app = VBoxLayoutExample()
    app.setOrientation(orient="vertical")
    app.run()
