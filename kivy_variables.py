# -*- coding: utf-8 -*-
"""
Created on Thu Mar  1 23:29:28 2018

@author: Tom
"""

# data
touch_data = []
csv_touch_data = []
touch_data_list = []
loaded_line = []
hover_data = []

# GUI variables
X_guideline = []
Y_guideline = []

# default options
screen_resolution_width = 800 #px
screen_resolution_height = 600 #px
save_load_prefix = "touch_data"
hoverdraw_tickrate = 1 #msec
guidelines_tickrate = 1 #sec
hover_key = "h"
clear_key = "c"
save_key = "s"
load_key = "l"