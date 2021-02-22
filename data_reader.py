# Author: Emanuel Ramirez Alsina
# Created: 02/09/2021


import csv

class DatabaseReader:
    ''' Main database data handler'''

    def __init__(self):
        ''' Init the basic database handler'''

        self.db_file = 'amazon_co-ecommerce_sample.csv'
        self.header = []

        # column headers that needs to be read from the db_file
        self.columns_to_read = [
            'uniq_id',
            'product_name',
            'number_of_reviews',
            'average_review_rating',
            'amazon_category_and_sub_category'
        ]

        # column headers that needs to be writen in the output file. Needed on both the GUI and cli version
        self.columns_to_write = [
            'input_item_type',
            'input_item_category',
            'input_number_to_generate',
            'output_item_name',
            'output_item_rating',
            'output_item_num_reviews'
        ]

        # column headers of the gui table. Only needed in GUI version of the application
        self.output_columns = [
            'product_name',
            'average_review_rating',
            'number_of_reviews'
        ]

        self.db_data = [] # database data structure


    def get_columns_to_write(self):
        ''' Returns the output.csv column headers that needs to be written'''
        return self.columns_to_write

    def get_output_columns(self):
        ''' Returns the GUI table column headers title'''
        return self.output_columns

    def get_database_filename(self):
        ''' Returns the name of the database file that is read to get the data from'''
        return self.db_file

    def get_categories(self):
        ''' Returns the lexicographically sorted categories found in the 'amazon_category_and_subcategory' column
            of the database file in a list format.

        :return example: ['3-D Puzzles', 'Accessories', 'Action Man', 'Activity Centres', 'Adults', 'Ages 3-4 Years', ...]
        '''
        return sorted({cat for row in self.db_data for cat in row['amazon_category_and_sub_category'] if cat})


    def get_data(self, filters=None):
        ''' Gets the each toy data from the database file and returns a list of dictionaries of each toy information found
            in the databse file.

        param: filters=list of a category and amount of toys to be searched for
        return: list of dictionaries where each dictionary represents a toy in the database file
                and each dictionary is composed of the following keys and their respective values:

                    uniq_id,
                    product_name,
                    manufacturer,price,
                    number_available_in_stock,
                    number_of_reviews,
                    number_of_answered_questions,
                    average_review_rating,
                    amazon_category_and_sub_category,
                    customers_who_bought_this_item_also_bought,
                    description,
                    product_information,
                    product_description,
                    items_customers_buy_after_viewing_this_item,
                    customer_questions_and_answers,
                    customer_reviews,sellers

                Note: the only categories saved on each dictionary of the list to be returned are the
                      categories found in the @self.columns_to_read.
        '''
        self.clear_data()
        with open(self.db_file, 'r', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file)
            self.header = next(reader)

            for toy in reader:
                toy_obj = {}
                for i, col in enumerate(self.header):
                    if col in self.columns_to_read:
                        toy_obj[col] = self.fix_data(col, toy[i])

                if filters:
                    # only add the toys that match the filter description
                    if filters[1] in toy_obj.get('amazon_category_and_sub_category'):
                        self.db_data.append(toy_obj)
                else:
                    self.db_data.append(toy_obj)

        return self.db_data

    def fix_data(self, key, value):
        ''' Recieves the key and value pair of a toy object and fix the format of the
            object data when needed.

        :return: the fixed value of the given @key
        '''

        if key == 'number_of_reviews':
            try:
                return int(value.replace(',', ''))

            except ValueError:
                return 0

        if key == 'average_review_rating':
            try:
                # original format is 'X.x out of X.x stars' we only want the X.x number as a float
                return float(value.split(' ')[0])

            except ValueError:
                return 0.0

        if key == 'amazon_category_and_sub_category':
            return value.split(' > ') # split the categories into a list friendly format

        return value

    def format_data_for_csv_writer(self, ifilter, data):
        ''' Prepares the data to be written according to spec to output.csv

            Formatted data example:
                ['toys', 'product_category', 'amount_of_toys', product_name', 'average_review_rating', 'number_of_reviews']

        param: ifilter=list of headers
        return: the formatted data
        '''
        result = []

        # add the filters
        for i, item in enumerate(data):
            result.append([ifilter[0], ifilter[1], ifilter[2], item.get('product_name'),
                           item.get('average_review_rating'), item.get('number_of_reviews')])

        return result

    def format_data_for_gui_output(self, data):
        ''' Prepares the data to be rendered in the GUI according to spec

            Each toy will be formatted with the values of the following keys of the current toy dictionary;
                ['product_name', 'average_review_rating', 'number_of_reviews']

        return: the formatted GUI data
        '''
        result = []
        for i, item in enumerate(data):
            result.append([item.get('product_name'), item.get('average_review_rating'), item.get('number_of_reviews')])
        return result


    def clear_data(self):
        ''' Clear the database and header data structures'''
        self.db_data.clear()
        self.header.clear()
