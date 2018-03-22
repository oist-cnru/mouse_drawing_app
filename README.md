# Mouse Drawing App v0.2.1
This is a simple GUI app for the generation of 2d mouse input data. It is built using Kivy, which means it can run on Linux, Windows, OS X, Android, iOS, and Raspberry Pi.

Demonstration video:

[![Demonstration of Tom's Mouse Drawing App v0.2](http://img.youtube.com/vi/pgXEHdsYymY/0.jpg)](http://www.youtube.com/watch?v=pgXEHdsYymY "Demonstration of Tom's Mouse Drawing App v0.2")

New features in v0.2:
- Automatic guidelines representing the half width, x = 0.5, and half height, y = 0.5, of the current screen. These guidlines are by default once per second.
- Hover draw, allowing you to toggle a on/off the collection of drawing data without holding down any mouse buttons. This has the advantage that when you hold the mouse in one place it continues to add more data points at that location, which may be useful for training a 'stay' behaviour for an RNN.
- Options menu allowing you to resize the screen to specific dimensions, change the default save/load filename prefix, update frequencies for the guidelines and hover draw functions, and change keybindings.

# Installation

Installation procedure:
1. Download/clone mouse_drawing_app
2. If you do not have Kivy installed, you will need to temporarily uninstall cython if its version is >=0.27 before proceding. This is because Kivy has some compilation issues with cython (see [here](https://kivy.org/docs/installation/deps-cython.html#known-issues)). After you have finished the installation, you can reinstall cython 0.27 or higher.
3. In the mouse_drawing_app directory, run 
```
python setup.py install
```
4. If the setup.py install is successful, you may proceed to [usage](#Usage). If it was not successful, you may need to manually install the Kivy package.

Required Python packages:
- Kivy
- Numpy
- Pandas

# Usage

Basic usage guide:
1. Run drawing_app.py.
```
python drawing_app.py
```
A small GUI window should open.

2. Click "Draw" to be taken to another screen with buttons on the top and a black background.
3. Click and drag your cursor to draw on the canvas. As you do, your cursor's relative position (X, Y) on the screen will be printed in the Python console. Position 0, 0 is Left, Bottom, and position 1, 1 is Right, Top.
4. When you release your cursor, the line drawing should stop.
5. Click the button labelled 'save' (or press 's' on your keyboard) to save the cursor positions you just drew (and which were just printed in the console) to a CSV file in the directory of drawing_app.py. By default, this file will be called "touch_data1.csv" (you can change the default filename in the options menu).
6. You may continue to draw and save a second file, i.e. "touch_data2.csv", and/or clear your current drawing at any point using the button labelled 'clear' (or by pressing 'c' on your keyboard).

Using other features:
- Hover draw: by default, press 'h' on your keyboard to start a hover drawing and press 'h' again to complete it.
- Loading drawings: currently, the load function just gets the most recently-saved drawing using the current filename and file index number, e.g. "touch_data1.csv". While the program is running, you can manually place and replace csv to load them as you wish.

# Bugs and issues

Buglist (as of 21 March 2018):
1. Clicking during the short fading animation between screens can cause the program to crash.
2. Keypresses don't register on the draw screen until there has been a touch on the screen.
3. Screen resolution is not updated in the options menu if the user manually changes the window size.
4. Copy/paste bugs in text fields of 'options' menu. This is a known Kivy issue (see [here](https://github.com/kivy/kivy/pull/5579) and [here](https://stackoverflow.com/questions/46057977/copy-text-from-texit-input)) and the fix will be available in the Kivy master branch soon (as of 21 March 2018).

Other known issues:
1. Incompatible with IPython/Jupyter Notebook (this is a general limitation of the Kivy module used in this app). It was possible to use Kivy in Jupyter Notebook since Kivy version 1.3.0 using InteractiveLauncher. However, this has been deprecated since version 1.10.0. Also see [here](https://stackoverflow.com/questions/36361742/connect-a-jupyter-notebook-to-a-running-python-app/).
2. When drawing_app.py is run from Spyder, you will need to set the run options so that it runs in a dedicated console. To do this, go to "Run" > "Configuration per file ..." or use Ctrl+F6 and under "Console" select "Execute in a dedicated console". When you run and then close the program, you will need to also close the new console terminal before re-launching (or execute drawing_app.py within a new console).
