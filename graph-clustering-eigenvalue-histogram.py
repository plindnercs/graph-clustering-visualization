# visualizes the output of the kpm library; eigenvalue histogram of a graph
# usage: python3 graph-clustering-eigenvalue-histogram.py input-file.txt (true | false)
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
is_y_log = sys.argv[2]

intervals, heights = read_input_file(input_file)

# flattening the intervals to get the bin edges
bin_edges = [interval[0] for interval in intervals] + [intervals[-1][1]]

plt.figure(figsize=(10, 6))
plt.hist(bin_edges[:-1], bins=bin_edges, weights=heights, edgecolor='black', align='left')

plt.xlabel('Value')
plt.ylabel('Height')
plt.title('Eigenvalue Histogram')

log_prefix = ''
if is_y_log == 'true' or is_y_log == 'TRUE' or is_y_log == 'True':
    plt.yscale('log')
    log_prefix += '_log'

timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
output_file = f"eigenvalue_histogram{log_prefix}_{timestamp}.png"

plt.savefig(output_file)

# plt.show()
