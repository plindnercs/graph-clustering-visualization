# visualizes the output of the kpm library; eigenvalue histogram of a graph
# usage: python3 graph-clustering-eigenvalue-histogram.py input-file.txt
import sys
import datetime
import matplotlib.pyplot as plt


def read_input_file(filename):
    intervals = []
    heights = []
    with open(filename, 'r') as file:
        for line in file:
            # parse line
            parts = line.strip().split('] ')
            interval_str = parts[0].strip('[')
            height = float(parts[1])

            interval = list(map(float, interval_str.split(',')))

            intervals.append(interval)
            heights.append(height)
    return intervals, heights


input_file = sys.argv[1]

intervals, heights = read_input_file(input_file)

# flattening the intervals to get the bin edges
bin_edges = [interval[0] for interval in intervals] + [intervals[-1][1]]

plt.figure(figsize=(10, 6))
plt.hist(bin_edges[:-1], bins=bin_edges, weights=heights, edgecolor='black', align='left')

plt.xlabel('Value')
plt.ylabel('Height')
plt.title('Eigenvalue Histogram')

plt.yscale('log')

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"eigenvalue_histogram_{timestamp}.png"

plt.savefig(output_file)

plt.show()
