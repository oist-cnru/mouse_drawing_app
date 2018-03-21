# mouse_drawing_app
simple gui app for the generation of 2d mouse input data

Required Python packages:
- Kivy
- Numpy
- Pandas

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

Other known issues:
1. Incompatible with IPython/Jupyter Notebook (this is a general limitation of the Kivy module used in this app). It was possible to use Kivy in Jupyter Notebook since Kivy version 1.3.0 using InteractiveLauncher (see documentation). However, this has been deprecated since version 1.10.0. Also see: https://stackoverflow.com/questions/36361742/connect-a-jupyter-notebook-to-a-running-python-app/
2. When drawing_app.py is run from Spyder, you will need to set the run options so that it runs in a dedicated console. To do this, go to "Run" > "Configuration per file ..." or use Ctrl+F6 and under "Console" select "Execute in a dedicated console". When you run and then close the program, you will need to also close the new console terminal before re-launching (or execute drawing_app.py within a new console).
