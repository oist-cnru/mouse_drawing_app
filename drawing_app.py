# -*- coding: utf-8 -*-
"""
Created on Thu Mar 1 21:47:57 2018

@author: Tom
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.config import Config
from kivy.graphics import Line, Color

import kivy_variables
from threading import Timer
import numpy as np
import pandas as pd
import os.path

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class Painter(Widget):
    
    def on_touch_down(self, touch):
        print("INFO: Touch begun!", touch.spos)
        kivy_variables.touch_data.append(touch.spos)
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y), group='touch_lines')
            
    def on_touch_move(self, touch):
        print(touch.spos)
        kivy_variables.touch_data.append(touch.spos)
        touch.ud["line"].points += (touch.x, touch.y)
		
    #def on_touch_up(self, touch):
    #    print("INFO: Touch released!")

class MainScreen(Screen):
    
    def exit_app(self):
        print("INFO: Exiting program.")
        Builder.unload_file("main.kv")
        App.get_running_app().stop()
        Window.close()

file_idx = 1

class OptionsScreen(Screen):
    
#    def __init__(self, **kwargs):
#        super(OptionsScreen, self).__init__(**kwargs)
#        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
#        self._keyboard.bind(on_key_down=self._on_keyboard_down)
#        
#    def _keyboard_closed(self):
#        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
#        self._keyboard = None
#    
#    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
#        print('INFO: The key', keycode, 'has been pressed')
#        if keycode[1] == kivy_variables.hover_key:
#            if not kivy_variables.touch_data:
#                print("INFO: Hover touch begun!")
#                self.hover_draw()
#            else:
#                self.t.cancel()
#                print("INFO: Hover touch ended!")
#        if keycode[1] == kivy_variables.clear_key:
#            self.on_release_clear()
#        if keycode[1] == kivy_variables.save_key:
#            self.save_csv()
#        if keycode[1] == kivy_variables.load_key:
#            self.load_csv()
    def on_release_clear_options(self):
        kivy_variables.touch_data = []
        self.root.ids.painter.canvas.clear()
        print("INFO: Data cleared.")
        if isinstance(kivy_variables.loaded_line, list):
            return
        self.canvas.remove_group('loaded_lines')
        kivy_variables.loaded_line = []
    
    def save_and_apply_options(self):
        if isinstance(self.ids.screen_resolution_width_option.text,str) & isinstance(self.ids.screen_resolution_height_option.text,str):
            kivy_variables.screen_resolution_width = self.ids.screen_resolution_width_option.text
            kivy_variables.screen_resolution_height = self.ids.screen_resolution_height_option.text
            Window.size = (int(kivy_variables.screen_resolution_width), int(kivy_variables.screen_resolution_height))
        if self.ids.save_load_prefix_option.text:
            if kivy_variables.save_load_prefix != self.ids.save_load_prefix_option.text:
                global file_idx
                file_idx = 1
            kivy_variables.save_load_prefix = self.ids.save_load_prefix_option.text
        if self.ids.hoverdraw_tickrate_option.text:
            kivy_variables.hoverdraw_tickrate = float(self.ids.hoverdraw_tickrate_option.text) #msec
        if self.ids.guidelines_tickrate_option.text:
            kivy_variables.guidelines_tickrate = float(self.ids.guidelines_tickrate_option.text) #sec
        if self.ids.hover_key_option.text:
            kivy_variables.hover_key = self.ids.hover_key_option.text
        if self.ids.clear_key_option.text:
            kivy_variables.clear_key = self.ids.clear_key_option.text
        if self.ids.save_key_option.text:
            kivy_variables.save_key = self.ids.save_key_option.text
        if self.ids.load_key_option.text:
            kivy_variables.load_key = self.ids.load_key_option.text
            
        #self._keyboard.bind(on_key_down=self._on_keyboard_down)

class DrawScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._dynamic_guidelines()
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('INFO: The key', keycode, 'has been pressed')
        if keycode[1] == kivy_variables.hover_key:
            if not kivy_variables.touch_data:
                print("INFO: Hover touch begun!")
                self.hover_draw()
            else:
                self.t.cancel()
                print("INFO: Hover touch ended!")
        if keycode[1] == kivy_variables.clear_key:
            self.on_release_clear()
            #self.canvas.ask_update()
            #kivy_variables.touch_data = []
            #self.ids.painter.canvas.clear()
            #print("canvas clear")
            #self.on_release_clear()
        if keycode[1] == kivy_variables.save_key:
            self.save_csv()
        if keycode[1] == kivy_variables.load_key:
            self.load_csv()

        return True # return True to accept the key. Otherwise, it will be used by the system.

    def _dynamic_guidelines(self):
        self.canvas.remove_group('guidelines')
        kivy_variables.X_guideline = []
        kivy_variables.Y_guideline = []
        if isinstance(kivy_variables.X_guideline, list):
            with self.canvas:
                Color(0.5,0.5,0.5,0.5)
                X_midpoint = 0.5 * Window.size[0]
                Y_midpoint = 0.5 * Window.size[1]
                kivy_variables.X_guideline = Line(points=[X_midpoint,0,X_midpoint,Y_midpoint*2], width=1, group='guidelines')
                kivy_variables.Y_guideline = Line(points=[0,Y_midpoint,X_midpoint*2,Y_midpoint], width=1, group='guidelines')
                Color(1,1,1,1)
        Timer(kivy_variables.guidelines_tickrate, self._dynamic_guidelines).start()

    def display_hover_draw(self):
        if kivy_variables.touch_data:
            with self.canvas:
                    kivy_variables.touch_data_list = kivy_variables.touch_data * np.array(Window.size)
                    kivy_variables.loaded_line = Line(points=np.concatenate(kivy_variables.touch_data_list).tolist(), width=1, group='loaded_lines')
            print("INFO: Hover touch data displayed.")
        else:
            print("WARN: No hover touch data was found to display!")

    def hover_draw(self):
        mouse_spos = np.array(Window.mouse_pos) / np.array(Window.size)
        print(mouse_spos)
        kivy_variables.touch_data.append(mouse_spos)
        self.t = Timer(kivy_variables.hoverdraw_tickrate/1000, self.hover_draw)
        self.t.start()
    
    def on_release_clear(self):
        kivy_variables.touch_data = []
        self.ids.painter.canvas.clear()
        print("INFO: Data cleared.")
        if isinstance(kivy_variables.loaded_line, list):
            return
        self.canvas.remove_group('loaded_lines')
        kivy_variables.loaded_line = []
        
    def save_csv(self):
        if not kivy_variables.touch_data:
            print("WARN: No data was found to save!")
        else:
            global file_idx
            line_filename = str(kivy_variables.save_load_prefix)+str(file_idx)+".csv"
            np.savetxt(line_filename, kivy_variables.touch_data, delimiter=",", fmt='%f')
            print("INFO: Data saved as '" + line_filename + "'.")
            file_idx += 1
    
    def load_csv(self):
        line_filename = str(kivy_variables.save_load_prefix)+str(file_idx-1)+".csv"
        if isinstance(kivy_variables.loaded_line, list):
            self.canvas.remove_group('loaded_lines')
        if os.path.exists(line_filename):
            kivy_variables.csv_touch_data = pd.read_csv(line_filename) * Window.size
            kivy_variables.touch_data = [tuple(x) for x in kivy_variables.csv_touch_data.values]
            kivy_variables.touch_data_list = [i for sub in kivy_variables.touch_data for i in sub]
            with self.canvas:
                kivy_variables.loaded_line = Line(points=kivy_variables.touch_data_list, width=1, group='loaded_lines')
            print("INFO: The file '" + line_filename + "' was loaded.")
        else:
            print("WARN: The file '" + line_filename + "' was not found!")

class ScreenManagement(ScreenManager):
    pass

presentation = Builder.load_file("main.kv")

class MainApp(App):
    
    def build(self):
        return presentation
    
    def callback(self, text):
        self.root.ids.textbox.text = "Hi"

if __name__ == "__main__":
    MainApp().run()