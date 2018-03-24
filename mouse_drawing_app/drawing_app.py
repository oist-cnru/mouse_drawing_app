# -*- coding: utf-8 -*-
"""
Created on Thu Mar 1 21:47:57 2018
Last saved on Thu Mar 22 14:55:00 2018

@author: Tom
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import FocusBehavior
from kivy.config import Config
from kivy.graphics import Line, Color

import kivy_variables
from threading import Timer
import numpy as np
import pandas as pd
import os.path

Config.set('input', 'mouse', 'mouse,multitouch_on_demand') # interpret all mouse and touch inputs, e.g. right mouse click, the same as left mouse click
file_idx = 1 # set our starting file index number for saving touch data, i.e. first file saved will be named "touch_data1.csv"

# create the Painter Widget class
class Painter(Widget):

    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        self.config_keyboard()

    def config_keyboard(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)   # sets a reference for an open keyboard
        self._keyboard.bind(on_key_down=self._on_keyboard_down)                 # binds the keyboard to keybindings described in _on_keyboard_down

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)   # unbinds the keyboard
        self._keyboard = None                                       # sets keyboard reference to None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print('INFO: The key', keycode, 'has been pressed')
        if keycode[1] == kivy_variables.hover_key:
            if not kivy_variables.touch_data:   # checks that touch data doesn't exist
                print("INFO: Hover touch begun!")
                self.hover_draw()               # if no touch data exists, start drawing
            elif hasattr(self, 't') :
                self.t.cancel()                 # if touch data exists, stop hover drawing
                self.display_hover_draw()       # display the hover touch data
                print("INFO: Hover touch ended!")
            else :
                print("WARN: Hover touch attempted to start, but touch data already exists!")
        if keycode[1] == kivy_variables.clear_key:
            self.on_release_clear()     # clear the canvas
        if keycode[1] == kivy_variables.save_key:
            self.save_csv()             # save the touch data
        if keycode[1] == kivy_variables.load_key:
            self.load_csv()             # load the most recently saved touch data
        return True     # return True to accept the key press, else it will be used by the system
    
    def on_release_clear(self):
        kivy_variables.touch_data = []  # clear the stored touch data
        self.canvas.clear()             # clear the canvas lines of touch lines
        print("INFO: Data cleared.")
        if isinstance(kivy_variables.loaded_line, list):    # if the loaded lines var = list (default before loading)
            return                                          # exit the function
        kivy_variables.loaded_line = []                     # else clear the stored loaded lines 
        self.canvas.remove_group('loaded_lines')            # and clear the canvas of loaded lines
    
    def hover_draw(self):
        mouse_spos = np.array(Window.mouse_pos) / np.array(Window.size)         # get x & y the mouse position relative to the size of the window, where 0,0 is left,bottom
        print(mouse_spos)                                                       # print the mouse position
        kivy_variables.touch_data.append(mouse_spos)                            # append it to the touch data
        self.t = Timer(kivy_variables.hoverdraw_tickrate/1000, self.hover_draw) # set a timer to wait some time, then re-execute this function
        self.t.start()                                                          # start the timer
        
    def display_hover_draw(self):
        if kivy_variables.touch_data:   # check that touch data exists
            with self.canvas:
                    kivy_variables.touch_data_list = kivy_variables.touch_data * np.array(Window.size)                                                  # create a list of the touch data and scale it by the window size
                    kivy_variables.loaded_line = Line(points=np.concatenate(kivy_variables.touch_data_list).tolist(), width=1, group='loaded_lines')    # draw the hover touch data on the canvas and consider it a 'loaded line' for the purposes of the clearing function
            print("INFO: Hover touch data displayed.")
        else:
            print("WARN: No hover touch data was found to display!")
            
    def save_csv(self):
        if not kivy_variables.touch_data:   # check that touch data exists
            print("WARN: No data was found to save!")
        else:
            global file_idx                                                                 # get the file index number for saving touch data
            line_filename = str(kivy_variables.save_load_prefix)+str(file_idx)+".csv"       # generate the csv filename to save as
            np.savetxt(line_filename, kivy_variables.touch_data, delimiter=",", fmt='%f')   # save it
            print("INFO: Data saved as '" + line_filename + "'.")
            file_idx += 1                                                                   # increase the file index number by one
    
    def load_csv(self):
        line_filename = str(kivy_variables.save_load_prefix)+str(file_idx-1)+".csv"         # get the most csv filename saved
        if isinstance(kivy_variables.loaded_line, list):    # check if there are any current loaded lines
            self.canvas.remove_group('loaded_lines')        # if there are, clear them from the canvas
        if os.path.exists(line_filename):                                                                                   # check the file exists
            kivy_variables.csv_touch_data = pd.read_csv(line_filename) * Window.size                                        # read the csv file as a pandas dataframe
            kivy_variables.touch_data = [tuple(x) for x in kivy_variables.csv_touch_data.values]                            # convert to tuples
            kivy_variables.touch_data_list = [i for sub in kivy_variables.touch_data for i in sub]                          # convert to list
            with self.canvas:
                kivy_variables.loaded_line = Line(points=kivy_variables.touch_data_list, width=1, group='loaded_lines')     # draw the loaded lines on the canvas
            print("INFO: The file '" + line_filename + "' was loaded.")
        else:
            print("WARN: The file '" + line_filename + "' was not found!")
    
    def on_touch_down(self, touch):                     # when there is a mouse touch down event
        self.config_keyboard()                          # configure the keyboard to enable keybinds, else they can maintain InputText focus from OptionsMenu, see https://github.com/oist-cnru/mouse_drawing_app/issues/5
        print("INFO: Touch begun!", touch.spos)
        kivy_variables.touch_data.append(touch.spos)    # add the relative mouse position to touch data
        with self.canvas:
            touch.ud["line"] = Line(points=(touch.x, touch.y), group='touch_lines')  # draw a line on the canvas
            
    def on_touch_move(self, touch):                     # when there is a mouse movement while touching
        print(touch.spos)
        kivy_variables.touch_data.append(touch.spos)    # add the new relative mouse positions to touch data
        touch.ud["line"].points += (touch.x, touch.y)   # and extend the drawn line on the canvas
		
    def on_touch_up(self, touch):
        print("INFO: Touch released!")

# create the Main Screen class
class MainScreen(Screen):
    
    # close down the program tidily
    def exit_app(self):
        print("INFO: Exiting program.")
        Builder.unload_file("main.kv")
        App.get_running_app().stop()
        Window.close()

# create the Options Screen class
class OptionsScreen(Screen):
    
    # let's users save and apply options, which are stored in the kivy_variables module for access across classes and are given default values there
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

class DrawScreen(Screen):

    def __init__(self, **kwargs):
        super(DrawScreen, self).__init__(**kwargs)
        self._dynamic_guidelines()

    # draws guidelines along x=0.5 and y=0.5
    def _dynamic_guidelines(self):
        self.canvas.remove_group('guidelines')              # remove any previous guidelines from the canvas
        kivy_variables.X_guideline = []                     # empty any previous guideline value for X
        kivy_variables.Y_guideline = []                     #                                    and Y
        if isinstance(kivy_variables.X_guideline, list):    # if the guideline value for X is a list (default empty state)
            with self.canvas:
                Color(0.5,0.5,0.5,0.5)                      # set the color of these guidelines to grey
                X_midpoint = 0.5 * Window.size[0]           # calculate x=0.5 for this window size
                Y_midpoint = 0.5 * Window.size[1]           # calculate y=0.5 for this window size
                kivy_variables.X_guideline = Line(points=[X_midpoint,0,X_midpoint,Y_midpoint*2], width=1, group='guidelines')  # draw X
                kivy_variables.Y_guideline = Line(points=[0,Y_midpoint,X_midpoint*2,Y_midpoint], width=1, group='guidelines')  # draw Y
                Color(1,1,1,1)                              # set the default color back to white (for drawing)
        Timer(kivy_variables.guidelines_tickrate, self._dynamic_guidelines).start()     # set and start a timer to re-call this function every kivy_variables.guidelines_tickrate (in seconds)
    
    # redefine the on_release_clear, save_csv, and load_csv functions so that they can be called by the Kivy buttons on the Draw Screen
    
    def on_release_clear(self):
        kivy_variables.touch_data = []  # clear the stored touch data
        self.ids.painter.canvas.clear()            # clear the canvas lines of touch lines
        print("INFO: Data cleared.")
        if isinstance(kivy_variables.loaded_line, list):    # if the loaded lines var = list (default before loading)
            return                                          # exit the function
        self.ids.painter.canvas.remove_group('loaded_lines')            # and clear the canvas of loaded lines
        kivy_variables.loaded_line = []                     # else clear the stored loaded lines 
        
    def save_csv(self):
        if not kivy_variables.touch_data:   # check that touch data exists
            print("WARN: No data was found to save!")
        else:
            global file_idx                                                                 # get the file index number for saving touch data
            line_filename = str(kivy_variables.save_load_prefix)+str(file_idx)+".csv"       # generate the csv filename to save as
            np.savetxt(line_filename, kivy_variables.touch_data, delimiter=",", fmt='%f')   # save it
            print("INFO: Data saved as '" + line_filename + "'.")
            file_idx += 1                                                                   # increase the file index number by one
    
    def load_csv(self):
        line_filename = str(kivy_variables.save_load_prefix)+str(file_idx-1)+".csv"         # get the most csv filename saved
        if isinstance(kivy_variables.loaded_line, list):    # check if there are any current loaded lines
            self.ids.painter.canvas.remove_group('loaded_lines')        # if there are, clear them from the canvas
        if os.path.exists(line_filename):                                                                                   # check the file exists
            kivy_variables.csv_touch_data = pd.read_csv(line_filename) * Window.size                                        # read the csv file as a pandas dataframe
            kivy_variables.touch_data = [tuple(x) for x in kivy_variables.csv_touch_data.values]                            # convert to tuples
            kivy_variables.touch_data_list = [i for sub in kivy_variables.touch_data for i in sub]                          # convert to list
            with self.ids.painter.canvas:
                kivy_variables.loaded_line = Line(points=kivy_variables.touch_data_list, width=1, group='loaded_lines')     # draw the loaded lines on the canvas
            print("INFO: The file '" + line_filename + "' was loaded.")
        else:
            print("WARN: The file '" + line_filename + "' was not found!")

# create the Screen Management class
class ScreenManagement(ScreenManager):
    pass # necessary for Kivy lang file (".kv" file)

# create the Main App class
class MainApp(App):
    pass # by default, this will load and build the "main.kv" file, see https://kivy.org/docs/api-kivy.app.html#kivy.app.App.load_kv

# starts running the app
if __name__ == "__main__":
    MainApp().run()
