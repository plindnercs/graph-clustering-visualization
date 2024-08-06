# computes the number of edges going from the output graph to the extracted graph
# usage: python3 graph-clustering-extracted-edges-count.py <input_file>

import sys

def count_total_number_of_edges(file_path):
    # read the content from the file
    with open(file_path, 'r') as file:
        input_text = file.read()

    # split the input text by lines
    lines = input_text.split('\n')

    total_count = 0

    for line in lines:
        if ':' in line:
            _, numbers = line.split(':', 1)
            # split the numbers by spaces and filter out any empty strings
            numbers_list = [num for num in numbers.split() if num.isdigit()]
            # add the count of numbers to the total count
            total_count += len(numbers_list)

    return total_count


input_file = sys.argv[1]
total_count = count_total_number_of_edges(input_file)
print(f"Total count of numbers after colons: {total_count}")
