# Author: Emanuel Ramirez Alsina
# Created: 02/11/2021

import csv_writer
import tkinter as tk
from data_reader import DatabaseReader
from tkinter import font
from tkinter import ttk
from sorter import sort_data

class App(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.data_handler = DatabaseReader()

        self.db_data = self.data_handler.get_data()

        self.categories = self.data_handler.get_categories()

        self.selected_category = tk.StringVar(self)
        self.number_of_toys = tk.StringVar(self)

        self.gui_headers = [
            'product_name',
            'average_review_rating',
            'number_of_reviews'
        ]

        self.csv_output_headers = [
            'input_item_type',
            'input_item_category',
            'input_number_to_generate',
            'output_item_name',
            'output_item_rating',
            'output_item_num_reviews'
        ]

        self.init_title('Life Generator')
        self.init_widget()
        self.init_button('Submit', self.generate_toys_table, 4, 0)
        self.init_button('Clear', self.clear_table, 4, 5)
        self.init_menu(self.selected_category)
        self.table = self.init_table()
        self.db_filtered_data = []



    def init_title(self, title):
        ''' Renders the @title in the frame'''
        label = tk.Label(self.root, text=title, font=('Arial', 36)).grid(row=0, column=0, columnspan=2)
        return label

    def init_widget(self):
        self.grid(padx=2, pady=2)
        self.input_num_of_toys('Number of toys: ', self.number_of_toys)


    def init_button(self, text, function, r, col):
        ''' Creates and handles interactions of the submit and clear buttons'''
        button = tk.Button(self, text=text, command=function)
        button.grid(row=r, column=col, columnspan=2, pady=(0,4))
        return button

    def init_menu(self, categories):
        ''' Initialized the dropdown menu of categories and handle the category selection'''
        label = tk.Label(self, text='Categories: ')
        label.grid(row=1, column=0, ipadx=30, sticky=tk.W)
        categories.set('Select Category')

        menu = tk.OptionMenu(self, categories, "",  *self.categories)
        menu.grid(row=1, column=5, ipadx=50, sticky=tk.W)

        return label, menu


    def input_num_of_toys(self, string, total):
        ''' Renders the entry box for the user to input the number of toys desired for output'''
        label = tk.Label(self, text='Number of toys: ')
        label.grid(row=2, column=0, ipadx=10)

        user_input = tk.Entry(self, width=5, textvariable=total)
        user_input.insert(tk.END, '0')
        user_input.grid(row=2, column=5, ipadx=50)

        return label, user_input

    def clear_table(self):
        ''' Clears the toys table from the GUI'''
        for toy in self.table.get_children():
            self.table.delete(toy)

    def init_table(self):
        ''' Initialized the toy display table'''
        cols = ('Product Name', 'Average Review Rating', 'Number of Reviews')
        table = ttk.Treeview(self.root, columns=cols, show='headings', height=25)

        for i, col in enumerate(cols):
            if col == 'Product Name':
                table.column(col, width=425, anchor='c')
            else:
                table.column(col, width=175, anchor='c')
            table.heading(col, text=col)
        table.grid(row=10, column=0, columnspan=2, sticky='ns')
        return table


    def generate_toys_table(self):
        ''' Generates the data for the display in the toys table'''
        self.clear_table()

        filters = ['toys', self.selected_category.get(), int(self.number_of_toys.get())]
        self.db_filtered_data = []

        self.db_filtered_data = self.data_handler.get_data(filters)

        self.db_filtered_data = sort_data(self.db_filtered_data, int(self.number_of_toys.get()))


        gui_formatted_data = self.data_handler.format_data_for_gui_output(self.db_filtered_data)

        self.display_data(gui_formatted_data, self.table)

        csv_formatted_data = self.data_handler.format_data_for_csv_writer(filters, self.db_filtered_data)

        csv_writer.write_output_file(filters, self.csv_output_headers, csv_formatted_data)


    def display_data(self, data, list_box):
        ''' Displays the data in the toys table in the GUI'''
        for i, toy in enumerate(data, start=1):
            list_box.insert('', 'end', values=(toy[0], toy[1], toy[2]))
