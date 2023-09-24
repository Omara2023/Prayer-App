#!python3
#prayer_times_modular - loads cities into widget and generates times for each.

from menu_widget_manager import MenuWidgetManager
from data_manager import DataManager

class MainWindow:
    '''A class to model the main menu.'''

    def __init__(self):
        ''''Initialise the main window, menu and layout.'''
        #Initialise the other classes for remaining components.
        self.widgets_manager = MenuWidgetManager()
        self.data_handler = DataManager()
        self.run_app()
     
    def clear_data(self):
        '''Delete data from SQL database.'''
        DataManager.reset_db()

    def run_app(self):
        '''Start tkinter app mainloop.'''
        self.widgets_manager.create_menu_widgets()
        self.widgets_manager.place_widgets()
        self.widgets_manager.root.mainloop()

if __name__ == '__main__':
    '''Instantiate the class and run the app normally'''
    widget = MainWindow()
    #widget.clear_data()
