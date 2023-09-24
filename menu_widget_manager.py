import tkinter as tk
from data_manager import DataManager
from city_list import CityList
from formatter_1 import Formatter
from location_window import LocationWindow

#Constants
ROW_LENGTH = 3

class MenuWidgetManager:
    '''Class to load/place widgets for the main menu and prayer displays.'''

    def __init__(self) -> None:
        '''Initialise attributes needed for window building.'''
        self.data_handler = DataManager()
        self.city_list = CityList(self.data_handler.return_cities('ref'), self.data_handler.return_cities('cities'))

    def create_menu_widgets(self):
        '''Instantiate widgets for main menu without placing them.'''
        self.root = tk.Tk()
        self.root.title('Prayer Widget Main Menu')
        self.root.geometry('600x400')

        self.menu_board = tk.LabelFrame(self.root, border=5)
        self.bottom_frame = tk.Frame(self.root)

        self.input_strip = tk.LabelFrame(self.bottom_frame)
        self.input_box = tk.Entry(self.input_strip, width=30)
        self.input_box.bind("<Return>", self.add_label)
        self.add_button = tk.Button(self.input_strip, text='Add', command=self.add_label)

    def place_widgets(self):
        '''Pack static elements and invoke label placing logic.'''
        self.menu_board.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.bottom_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        self.input_strip.pack()
        self.input_box.pack(side=tk.LEFT)
        self.add_button.pack()

        self.reload_menu_options()

    def add_label(self, *args):
        '''Add text in entry to CityList if appropriate and update display.'''
        text = self.input_box.get()
        self.input_box.delete(0, "end")
        if not (text is None):
            self.city_list.append((input := Formatter.format(text)))
            if input in self.city_list:
                self.data_handler.manage_city_list('add', Formatter.sanitise(text))
                self.reload_menu_options()

    def remove_label(self, index):
        '''Remove item from CityList and remove its label from display.'''
        location = self.city_list[index]
        self.data_handler.manage_city_list('delete', location)
        del self.city_list[index]

        self.reload_menu_options()

    def reload_menu_options(self):
        '''(Re)create and place labels to main menu board.'''
        for child in self.menu_board.winfo_children():
            child.destroy()

        for index, value in enumerate(self.city_list):
            label_frame = tk.Label(master=self.menu_board, padx=10, pady=10, relief=tk.SOLID, bd=1)
            label_frame.grid(row= index // ROW_LENGTH, column= index % ROW_LENGTH, padx=5, pady=5)

            label = tk.Label(label_frame, text=value, anchor=tk.W, wraplength=200, padx=10)
            label.bind("<Button-1>", lambda event: self.load_location_window(event))
            label.pack(side=tk.LEFT, padx=5, pady=5)

            delete_button = tk.Button(label_frame, text="X", 
                                      command= lambda index=index: self.remove_label(index))
            delete_button.pack(side=tk.RIGHT, padx=(0, 5), pady=5)
    
    def load_location_window(self, event: tk.Event):
        '''Load individual location prayer screen.'''
        location = Formatter.sanitise(event.widget['text'])
        LocationWindow(location)