# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 23:29:28 2018
Last saved on Wed Mar 21 23:50:00 2018

@author: Tom
"""

# data
touch_data = []
csv_touch_data = []
touch_data_list = []
loaded_line = []
hover_data = []

# GUI variables for guidelines
X_guideline = []
Y_guideline = []

# default options
screen_resolution_width = 800      # in pixels
screen_resolution_height = 600     # in pixels
save_load_prefix = "touch_data"
hoverdraw_tickrate = 1             # in milliseconds
guidelines_tickrate = 1            # in seconds
hover_key = 'h'
clear_key = 'c'
save_key = 's'
load_key = 'd'