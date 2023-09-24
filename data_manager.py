import sqlite3
import requests
import bs4
import json
from typing import Union
from typing_extensions import Literal
from formatter_1 import Formatter

#Constants
DB_NAME = 'prayer_widget.db'
CITY_URL = 'https://ontheworldmap.com/all/cities/'
API_URL = 'https://api.aladhan.com/v1/timingsByAddress/{}?address={}&school=1&method=15'
CITIES_JSON = 'table-data.json'
PRAYERS = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']

class DataManager:
    '''Class to execute SQl commaands, read data and execute Web-APIs.'''

    def __init__(self) -> None:
        '''Setup SQL table connections.'''
        self.conn = sqlite3.connect(DB_NAME)
        list(map(self.create_city_table, ('ref', 'cities')))

    def create_city_table(self, mode: str):
        '''Create an all-cities table if it doesn't already exist..'''

        assert mode in ('ref', 'cities')
        cursor = self.conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {mode} (
                id INTEGER PRIMARY KEY,
                city TEXT
            )''')
        
        self.conn.commit()

    def create_prayer_table(self, location):
        '''Create table for location to store its times.'''

        cursor = self.conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{location}" (
                date TEXT PRIMARY KEY,
                Fajr TEXT,
                Dhuhr TEXT,
                Asr TEXT,
                Maghrib TEXT,
                Isha TEXT
            )''')
        self.conn.commit()

    def return_cities(self, mode: Union[str, Literal['ref', 'cities']]):
        '''Read from SQL table and return list of cities based on mode.'''
        assert mode in ('ref', 'cities')
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT city from {mode}')
        rows = cursor.fetchall()
        if rows:
            return [Formatter.format(tup[0]) for tup in rows]
        elif mode == 'ref':
            cities = self.web_scrape_cities()
            print('Downloading reference city data from web')
            cursor.executemany('INSERT INTO ref (city) VALUES (?)', 
                               ([(Formatter.sanitise(city),) for city in cities]))
            self.conn.commit()
            return [Formatter.format(city) for city in cities]
        else:
            #Aka no cities and we weren't after a reference list; equivalent to blank menu.
            return []

    def load_prayer_times(self, location: str, date: str):
        '''Exexcute SELECT statement to obtain/return list of timing strings.'''
        cursor = self.conn.cursor()
        cursor.execute(f'SELECT * FROM "{location}" WHERE date=?', (date,))
        row = cursor.fetchone()
        if row:
            return row[1:]
        return None

    def download_prayer_times(self, date: str, location):
        '''Obtain .json data from Web-API and return list/None.'''
        try:
            response = requests.get(API_URL.format(date, location))
            response.raise_for_status()
            timings = [response.json()['data']['timings'].get(prayer) for prayer in PRAYERS]
            self.save_prayer_times(timings, location, date)
            return timings
        except requests.HTTPError:
            print(f'Could not obtain data from the API for date {date}')
            return None

    def save_prayer_times(self, prayer_times, location, date: str):
        '''Insert newly downloaded timings into respective location table.'''
        cursor = self.conn.cursor()
        cursor.execute(f'REPLACE INTO "{location}" VALUES (?, ?, ?, ?, ?, ?)',
                       (date, *prayer_times))
        self.conn.commit()

    def manage_city_list(self, action, location):
        '''Ammend SQL database depending on the mode; adding or removing cities.'''
        cursor = self.conn.cursor()
        if action == 'add':
            cursor.execute('INSERT INTO cities (city) VALUES (?)', (location,))
            self.create_prayer_table(location)
        elif action == 'delete':
            cursor.execute('DELETE FROM cities WHERE city=?', (location,))
            cursor.execute(f'DROP TABLE IF EXISTS "{location}"')

        self.conn.commit()

    def reset_db(self):
        '''Empties all tables in sql.db file.'''
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        for table in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table[0]}')

        self.conn.commit()
        print('Database successfully purged.')

    def web_scrape_cities(self):
        '''Download city json data via API and return list/none.'''
        try:
            response = requests.get(CITY_URL)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.content, features='html.parser')
            return [tag.text for tag in soup.select('div.col-3 li')]
        except requests.HTTPError:
            print('List download failed. Loading from the capital city file.')
            return self.load_backup_cities()
        except requests.ConnectionError:
            print('No internet connection. Loading from the capital city file.')
            return self.load_backup_cities()

    def load_backup_cities(self):
        '''Read city reference data from packaged JSON file.'''
        try:
            with open(CITIES_JSON, 'r') as json_file:
                data = json.load(json_file)
            return [i['capital'] for i in data]
        except FileNotFoundError:
            print('Unable to obtain the city list for input validation.')
            return None
        
    def close(self):
        '''Terminate SQL database connection.'''
        self.conn.close()
        
if __name__ == '__main__':
    '''Instantiate the class to remove clear the tables.'''
    DataManager().reset_db()