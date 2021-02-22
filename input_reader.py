# Author: Emanuel Ramirez Alsina
# Created: 02/10/2021

import csv

class Filters:
    ''' Main input handler from both cli argument or GUI interactions'''

    def __init__(self, cli_filename=None):
        ''' Initializes input_reader

        param: filename=input.csv or None

        '''
        self.filters = []
        self.header = []
        self.num_of_toys = 0

        # recevied input.csv as argument
        if cli_filename:
            self.get_filters_from_input(cli_filename)

    def get_filters_from_input(self, filename):
        '''
        Example output:
            Headers: ['input_item_type', 'input_item_category', 'input_number_to_generate']
            Filters: [['toys', 'Hobbies', '3'], ['toys', 'Worlds Apart', '5'], ['clothes', 'Garments', '22']]
        '''
        if not filename:
            print('File not found.')

        self.header, self.filters = [],[]
        with open(filename, encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            self.header = next(reader)

            self.filters = next(reader)

        self.num_of_toys = int(self.filters[2])
        return (self.header, self.filters)

    def get_num_of_toys(self):
        ''' Returns the current number of toys asked from the user'''
        return self.num_of_toys

    def clear_filters(self):
        ''' Clears the filtes data structure'''
        return self.filters.clear()

    def clear_header(self):
        ''' Clears the header data structure'''
        return self.header.clear()
