from kivy.app import App
from kivy.uix.button import Button
from kivy.base import EventLoop 
  
class Hello(App):
    def build(self):
        btn = Button(text='Hello World 2', color=(1, 1, 0, 1), background_color=(255, 255, 255, 255))
        return  btn
  
Hello().run()
