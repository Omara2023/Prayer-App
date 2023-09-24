import datetime

class Formatter:
    '''Class to store methods that format and sanitise strings.'''
    
    @classmethod
    def sanitise(cls, string: str):
        '''Return lowercase and remove spaces.'''
        return string.lower().replace(' ', '_')
    
    @classmethod
    def format(cls, string: str):
        '''Return titled string with spaces restored.'''
        return string.title().replace('_', ' ')
    
    @classmethod
    def full_date(cls, date: datetime.datetime):
        '''Return a full date.'''
        return date.strftime("%A %d of %B %Y")
    
    @classmethod
    def short_date(cls, date: datetime.datetime):
        '''Return the shortened date.'''
        return date.strftime("%d-%m-%Y")