# Author: Emanuel Ramirez Alsina
# Created: 02/09/2021

import cli
import gui
import sys
import tkinter as tk

DATABASE_FILE = 'amazon_co-ecommerce_sample.csv'

def main():
    ''' Program main driver call cli.py if input file is given. Calls the gui builder
        if no input argument is received
    '''

    # CLI application
    if len(sys.argv) > 1:
        input_file = str(sys.argv[1])
        cli.run(DATABASE_FILE, input_file)

    # GUI application
    else:
        root = tk.Tk()
        root.geometry('800x800')
        app = gui.App(root)
        app.mainloop()


if __name__ == '__main__':
    main()
