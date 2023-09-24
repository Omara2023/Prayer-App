from formatter_1 import Formatter

class CityList(list):
    '''List of cities class - manages I/O and sanitizing.'''

    def __init__(self, reference_list, *args) -> None:
        '''Initialise Data Structure.'''
        super().__init__()
        self.reference_list = reference_list

        if len(args) == 1 and isinstance(args[0], (list, tuple)):
            args = args[0]
        for i in args:
            if isinstance(i, str):
                self.append(i)
            else:
                print(f'Object {i}, type {type(i)} cannot be added to this list.')

    def append(self, __object: str) -> None:
        '''Extend default append to only add verified objects, correctly formatted.'''
        if self.validate_string(__object):
            super().append(Formatter.format(__object))
        
    def extend(self, __object: (list, tuple)):
        '''Extend default extend to only add verified objects, correctly formatted.'''
        if isinstance(__object, (list, tuple)):
            for item in __object:
                if not self.validate_string(item):
                    return 
            super().extend([Formatter.format(item) for item in __object])
        
    def validate_string(self, city_string: str):
        '''Return if test string is included in acceptable names.'''    
        if not (ref := self.reference_list) is None:
            # Convert city_string to lowercase for case-insensitive comparison
            city_string_lower = city_string.lower()
            return any(city_string_lower == city.lower() for city in ref) or any([city_string_lower in city.lower() for city in ref]) 
        else:
            return None
        
    def __getitem__(self, index):
        '''Ensures indexed items are sanitized on access.'''
        item = super().__getitem__(index)
        return Formatter.sanitise(item)