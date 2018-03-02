# -*- coding: utf-8 -*-
"""
Created on Thu Feb  15 21:47:57 2018

@author: Tom
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.widget import Widget
from kivy.graphics import Line

import Global
import numpy as np

class Painter(Widget):
    
    def on_touch_down(self, touch):
        print(touch.spos)
        Global.touch_data.append(touch.spos)
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y))
            
    def on_touch_move(self, touch):
        print(touch.spos)
        Global.touch_data.append(touch.spos)
        touch.ud["line"].points += (touch.x, touch.y)
		
    def on_touch_up(self, touch):
        print("RELEASED!",touch.spos)

class MainScreen(Screen):
    pass

file_idx = 1

class AnotherScreen(Screen):
    
    def on_release_clear(self):
        Global.touch_data = []
        
    def on_release_save(self):
        global file_idx
        np.savetxt("touch_data"+str(file_idx)+".csv", Global.touch_data, delimiter=",", fmt='%f')
        file_idx += 1

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    
    def build(self):
        return presentation

if __name__ == "__main__":
    MainApp().run()