import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os
import sys
from datetime import datetime

# Set the QT_QPA_PLATFORM environment variable
os.environ['QT_QPA_PLATFORM'] = 'wayland'

# Import your Qt-based modules after setting the environment variable
from PyQt5.QtCore import QThread, QObject, pyqtSignal

def read_triples_from_file_numpy(file_path):
    with open(file_path, 'r') as file:
        # Iterate until the "*****" line is found
        sawStarsOnce = False
        for line in file:
            if line.strip() == "*****":
                if sawStarsOnce:
                    break
                sawStarsOnce = True

        # The next line contains the number of triples
        num_triples = int(next(file).strip())

        # Preallocate a NumPy array of the right size
        triples = np.empty((num_triples, 3), dtype=int)

        # Read and store each triple directly into the NumPy array
        for i in range(num_triples):
            line = next(file).strip()
            parts = line.split(',')
            if len(parts) == 3:
                try:
                    triples[i] = np.array(parts, dtype=int)
                except ValueError:
                    # Handle the case where a line doesn't contain valid integers
                    print(f"Warning: Line '{line}' does not contain valid integers. Skipping.")
                    i -= 1  # Adjust the index to account for the skipped line
    return triples



if __name__ == '__main__':
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Started computation")

    # Example usage
    file_compared_pairs = "graph-clustering-3d-histogram-member-overlap-parallel.sh.o274603"

    with open(r'ig_communities_output_120h.metis', 'r') as fp:
        file = fp.readlines()

    # create 4-tupel for every community
    # ( community id | number of members | size of overlap | members of community as set )
    communities = {k: [k, len(file[k].replace('\n', '').split(' ')), 0, set(file[k].replace('\n', '').split(' '))] for k in range(0, len(file))}

    # first read all triples to get max_overlap
    triples = read_triples_from_file_numpy(file_compared_pairs)
    max_overlap = np.max(triples[:, 2])
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Found max overlap: " + str(max_overlap))
    triples = None

    # determine the max value of the community size
    max_community_size = 0
    for community_id, community_info in communities.items():
        max_community_size = max(max_community_size, community_info[1])
        # Find max overlap size from triples
        # This requires processing the triples file line by line
        # Placeholder for processing triples file to find max_overlap

    # Initialize a 3D array for counts
    counts = np.zeros((max_community_size + 1, max_overlap + 1), dtype=np.int32)

    # Process triples and update counts immediately
    with open(file_compared_pairs, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 3:
                try:
                    triple = np.array(parts, dtype=int)
                    community1_size = communities[triple[0]][1]
                    community2_size = communities[triple[1]][1]
                    overlap_size = triple[2]
                    counts[community1_size, overlap_size] += 1
                    counts[community2_size, overlap_size] += 1
                except ValueError:
                    continue

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Prepared data for 3d plot")

    # Create the 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Create the x, y, and z coordinates
    xpos, ypos = np.meshgrid(np.arange(counts.shape[1]), np.arange(counts.shape[0]))
    xpos = xpos.flatten()
    ypos = ypos.flatten()
    zpos = np.zeros_like(xpos)

    # Create the dx, dy, dz for bar sizes
    dx = dy = np.ones_like(zpos)
    dz = counts.flatten()

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Created axis for 3d plot")

    ax.bar3d(xpos, ypos, zpos, dx, dy, dz)

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Created 3d bar diagram")

    ax.set_xlabel('Size of Overlap')
    ax.set_ylabel('Size of Community')
    ax.set_zlabel('Number of Overlaps')

    # Save the plot to a file with the current date and time
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"3d_plot_{current_time}.png"
    plt.savefig(file_name)
