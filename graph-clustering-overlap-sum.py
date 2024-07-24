# calculates number of total overlaps from triple file structured as: overlap_size, community_size, number_of_overlaps
# usage: python3 graph-clustering-overlap-sum.py triples_2024_02_12_14_02_40.txt

import sys
import numpy as np

def read_triples_from_file_numpy(file_path, num_triples):
    with open(file_path, 'r') as file:
        # preallocate a NumPy array of the right size
        triples = np.empty((num_triples, 3), dtype=int)

        # read and store each triple directly into the NumPy array
        for i in range(num_triples):
            line = next(file).strip()
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    triples[i] = np.array(parts, dtype=int)
                except ValueError:
                    # handle the case where a line doesn't contain valid integers
                    print(f"Warning: Line '{line}' does not contain valid integers. Skipping.")
                    i -= 1  # adjust the index to account for the skipped line
    return triples


file_triples = sys.argv[1]

num_lines = 0
with open(file_triples, "rb") as f:
    num_lines = sum(1 for _ in f)

triples = read_triples_from_file_numpy(file_triples, num_lines - 1)

print("Sum of overlaps: " + str(np.sum(triples[:, 2])))