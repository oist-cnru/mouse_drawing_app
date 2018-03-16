# mouse_drawing_app
simple gui app for the generation of 2d mouse input data

Required Python packages:
- Kivy
- Numpy

Installation procedure:
1. run setup.py

Basic usage guide:
1. Run drawing_app.py. A small GUI window should open.
2. Click "Draw" to be taken to a second screen with buttons on the top and a black background.
3. Click and drag your cursor to draw on the canvas. As you do, your cursor's relative position (X, Y) on the screen will be printed in the Python console.
4. When you release your cursor, the line drawing should stop.
5. Click the button labelled 'save' to save the cursor positions you just drew (and which were just printed in the console) to a CSV file in the directory of drawing_app.py. This file will be called "touch_data1.csv".
6. You may continue to draw and save a second file, i.e. "touch_data2.csv", and/or clear your current drawing at any point using the button labelled 'clear'.

Buglist (as of 16 March 2018):
1. Copy/paste bugs in text fields of 'options' menu. This is a known Kivy issue (https://github.com/kivy/kivy/pull/5579, https://stackoverflow.com/questions/46057977/copy-text-from-texit-input) and the fix will be available in the Kivy master branch soon (as of 16 March 2018).

2. Cannot re-bind keys

3. Keybinds do not affect screen, e.g. clear, but can affect the variables.
https://stackoverflow.com/questions/32827495/kivy-make-buttons-change-the-text-of-textinput

Other known issues:
1. Not compatible with IPython/Jupyter Notebook (this is a general limitation of the Kivy module used in this app)
