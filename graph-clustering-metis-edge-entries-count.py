# computes the number of edge entries inside a metis file
# usage: python3 graph-clustering-metis-edge-entries-count.py <input_file>

import sys


def count_edge_entries(file_path):
    with open(file_path, 'r') as file:
        # read all lines from the file
        lines = file.readlines()

    total_count = 0

    # iterate through each line except the first (header) line
    for line in lines[1:]:
        # strip leading/trailing whitespace and split by whitespace
        entries = line.strip().split()
        total_count += len(entries)

    return total_count


input_file = sys.argv[1]
edge_entries_count = count_edge_entries(input_file)
print(f"Total number of edge entries: {edge_entries_count}")