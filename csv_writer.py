
import csv
import os.path

def write_output_file(filters, output_header, data):
    ''' Writes the data to a file named output.csv'''

    output_file = 'output.csv'

    with open(output_file, 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(output_header) # write headers to csv

        for line in data:
            writer.writerow([str(col) for col in line])
