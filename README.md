# mouse_drawing_app
simple gui app for the generation of 2d mouse input data

Basic usage guide:
1. Run drawing_app.py. A small GUI window should open.
2. Click within the window. You should be taken to a second screen with three buttons on the top and a black background.
3. Click and drag your cursor to draw on the canvas. As you do, your cursor's relative position (X, Y) on the screen will be printed in the Python console.
4. When you release your cursor, the line drawing should stop.
5. Click the button labelled 'save' to save the cursor positions you just drew (and which were just printed in the console) to a CSV file in the directory of drawing_app.py. This file will be called "touch_data1.csv".
6. You may continue to draw and save a second file, i.e. "touch_data2.csv", and/or clear your current drawing at any point using the button labelled 'clear'.

Known issues:
1. When you close the app you will need to restart your Python terminal or run the app in a new terminal. This is because Kivy does not listen to the (out of window) exiting.
2. Not compatible with IPython/Jupyter Notebook (this is a general limitation of the Kivy module used in this app)

Ideas for future features:
- Add an 'exit' button which Kivy listens to so known issue 1 doesn't occur.
- Add a 'load' feature to load previous drawings from the csv files
- Add an 'erase' feature to erase individual points of the drawing or entire, connected lines
