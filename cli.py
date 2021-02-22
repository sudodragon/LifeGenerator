# Author: Emanuel Ramirez Alsina
# Created: 02/10/2021

from data_reader import DatabaseReader
from input_reader import Filters
from sorter import sort_data
from csv_writer import write_output_file

def run(db_file, input_file):
    ''' Runs the cli application side of the program because an input file was received

    :param: input_file: input.csv file containing the filtering data
    '''
    filter_handler = Filters()      # init input_reader
    data_handler = DatabaseReader() # init data_reader

    headers, filters = filter_handler.get_filters_from_input(input_file)

    # filter should be in the format ['toys', input_item_category, number_to_generate]
    db_data = data_handler.get_data(filters)

    db_data = sort_data(db_data, filter_handler.get_num_of_toys())

    output_headers = data_handler.get_columns_to_write()
    formatted_data = data_handler.format_data_for_csv_writer(filters, db_data)


    if len(formatted_data) == 0:
        print('No matches found in the database.')
    else:
        write_output_file(filters, output_headers, formatted_data)

    filter_handler.clear_filters()
    filter_handler.clear_header()
