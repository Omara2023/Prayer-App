import datetime
import tkinter as tk
from data_manager import DataManager
from formatter_1 import Formatter

#Constants
PRAYERS = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']

class LocationWindow:
    '''Class to model the prayer time display itself that loads from the menu.'''

    def __init__(self, location):
        '''Initialise the Prayer Window with time and place states.'''
        self.location = location
        self.db = DataManager()
        self.current_date = datetime.datetime.now()
        self.times = None

        self.setup_gui()
        self.adjust_date()            

    def setup_gui(self):
        '''Instantiates and places widgets for location times.'''
        self.root = tk.Toplevel()
        self.root.title(f'{Formatter.format(self.location)} Times')
        self.root.geometry('280x240')
        self.root.protocol("WM_DELETE_WINDOW", self.close_screen)

        self.title_label = tk.Label(self.root, pady=10)
        self.label_objs = [tk.Label(self.root) for _ in PRAYERS]

        for x in [self.title_label, *self.label_objs]:
            x.pack()

        prev_button = tk.Button(self.root, text="< Previous", 
                                command=lambda: self.adjust_date(-1))
        next_button = tk.Button(self.root, text="Next >", 
                                command=lambda: self.adjust_date(1))

        prev_button.pack(side="left", padx=10)
        next_button.pack(side="right", padx=10)

    def adjust_date(self, days=0):
        '''Increment/decrease the date.''' 
        self.current_date += datetime.timedelta(days=days)
        self.reload_labels()

    def reload_labels(self):
        '''Configure the text for the time labels'''
        date_str = Formatter.short_date(self.current_date)
        times = self.db.load_prayer_times(self.location, date_str)

        if not (times is None):
            self.times = times
        elif not (times := self.db.download_prayer_times(date_str, self.location)) is None:
            self.times = times
        else:
            print('Failed to load times from database or Web-API.')
            return
        
        self.title_label.config(text=Formatter.full_date(self.current_date))
        for label_obj, prayer, time in zip(self.label_objs, PRAYERS, self.times):
            label_obj.config(text=f'{prayer}: {time}')

    def close_screen(self):
        '''Manage SQL connection cleanup on window exit.'''
        self.db.close()
        self.root.destroy()

#Note to self - add a prayer class with tk.labels and load 5 of those per screen to trim down methods.