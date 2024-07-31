# visualization of overlaps based on triples: community1_id, community2_id, overlap_size
# usage: python3 graph-clustering-3d-histogram-visualization.py graph-clustering-3d-histogram-member-overlap-parallel.sh.o276078 ig_communities_output_120h.metis onMach2 (true | false)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
from datetime import datetime
import plotly.graph_objects as go



def read_triples_from_file_numpy(file_path, on_mach2):
    with open(file_path, 'r') as file:
        # iterate until the "*****" line is found (needed for output on mach2)

        if on_mach2 == 'true':
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


def create_bar_mesh(x, y, z, dx, dy, dz):
    def cube_vertices(x, y, z, dx, dy, dz):
        return np.array([
            [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]
        ])

    vertices = []
    for xi, yi, zi, dxi, dyi, dzi in zip(x, y, z, dx, dy, dz):
        vertices.append(cube_vertices(xi, yi, zi, dxi, dyi, dzi))

    # Each bar consists of 12 triangles (2 per face)
    faces = []
    for i in range(len(x)):
        offset = i * 8  # Each cube has 8 vertices
        faces.extend([
            [offset, offset+1, offset+2], [offset, offset+2, offset+3],  # Front face
            [offset+4, offset+7, offset+6], [offset+4, offset+6, offset+5],  # Back face
            [offset, offset+3, offset+7], [offset, offset+7, offset+4],  # Left face
            [offset+1, offset+5, offset+6], [offset+1, offset+6, offset+2],  # Right face
            [offset, offset+4, offset+5], [offset, offset+5, offset+1],  # Bottom face
            [offset+3, offset+2, offset+6], [offset+3, offset+6, offset+7]  # Top face
        ])

    # Flatten the vertices array
    vertices = np.array(vertices).reshape(-1, 3).T

    return vertices, faces


file_compared_pairs = sys.argv[1]
file_communities = sys.argv[2]
on_mach2 = sys.argv[3]

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print(current_time + ": Started computation")

with open(file_communities, 'r') as fp:
    file = fp.readlines()

# create 4-tupel for every community
# ( community id | number of members | size of overlap | members of community as set )
communities = {k: [k, len(file[k].replace('\n', '').split(' ')), 0, set(file[k].replace('\n', '').split(' '))] for k in range(0, len(file))}

# first read all triples to get max_overlap
triples = read_triples_from_file_numpy(file_compared_pairs, on_mach2)

max_overlap = np.max(triples[:, 2])

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print(current_time + ": Found max overlap: " + str(max_overlap))

# determine the max value of the community size
max_community_size = 0
for community_id, community_info in communities.items():
    max_community_size = max(max_community_size, community_info[1])

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print(current_time + ": Found max community size: " + str(max_community_size))

# Initialize a 3D array for counts
counts = np.zeros((max_community_size + 1, max_overlap + 1), dtype=np.int32)

# Process triples and update counts immediately
i = 0
print("length of triples: " + str(len(triples)))
for triple in triples:
    community1_size = communities[triple[0]][1]
    community2_size = communities[triple[1]][1]
    overlap_size = triple[2]
    counts[community1_size, overlap_size] += 1
    counts[community2_size, overlap_size] += 1

# print("total sum of counts: " + str(np.sum(counts)))

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
print(current_time + ": Prepared data for 3d plot")

triples = None
communities = None

# Create the 3D plot with Plotly
fig = go.Figure()

# print(counts)

if True:
    # Define the range for the subset
    x_range = max_overlap + 1  # Adjust as needed
    y_range = max_community_size + 1 # Adjust as needed

    # Create the x, y coordinates for the subset
    xpos_subset, ypos_subset = np.meshgrid(np.arange(x_range), np.arange(y_range ))
    xpos_subset = xpos_subset.flatten()
    ypos_subset = ypos_subset.flatten()

    # Select the counts for the subset and then flatten
    counts_subset = counts[:y_range, :x_range].flatten()

    # print(counts_subset)

    # Filter out zero values from the subset
    non_zero_indices_subset = counts_subset != 0
    xpos_filtered = xpos_subset[non_zero_indices_subset]
    ypos_filtered = ypos_subset[non_zero_indices_subset]
    dz_filtered = counts_subset[non_zero_indices_subset]

    # print(non_zero_indices_subset)

    vertices, faces = create_bar_mesh(xpos_filtered, ypos_filtered, np.zeros_like(dz_filtered),
                                      np.ones_like(xpos_filtered), np.ones_like(ypos_filtered), dz_filtered)

    # Generate colors for each face
    colors = ['blue'] * len(faces)

    fig.add_trace(go.Mesh3d(
        x=vertices[0], # X-coordinates of vertices
        y=vertices[1], # Y-coordinates of vertices
        z=vertices[2], # Z-coordinates of vertices
        i=[f[0] for f in faces],
        j=[f[1] for f in faces],
        k=[f[2] for f in faces],
        opacity=1,
        facecolor=colors#,  # Array of colors for each face
        #hoverinfo='none'
    ))

    # Add invisible Scatter3d trace for hover info
    hover_text = [f"Overlap Size: {x}, Community Size: {y}, Count: {z}" for x, y, z in zip(xpos_filtered, ypos_filtered, dz_filtered)]
    fig.add_trace(go.Scatter3d(
        x=xpos_filtered,
        y=ypos_filtered,
        z=dz_filtered,
        mode='markers',
        marker=dict(size=5, opacity=0),
        text=hover_text,
        hoverinfo='text'
    ))

    # Save the triples to a file (for generating a model based on the data)
    triples_file_name = f"triples_{current_time}.txt"
    with open(triples_file_name, 'w') as file:
        for x, y, z in zip(xpos_filtered, ypos_filtered, dz_filtered):
            file.write(f"{x}, {y}, {z}\n")

    print(current_time + ": Saved triples to " + triples_file_name)

    fig.update_layout(
        scene=dict(
            xaxis_title='Size of Overlap',
            yaxis_title='Size of Community',
            zaxis=dict(
                title='Number of Overlaps',
                type='log',
                range=[np.log10(1), np.log10(np.max(dz_filtered) + 1)] # Adjust the log range
                # range=[np.log10(1), np.log10(np.max(dz_filtered) + 1)] # shows all values on z-axis
            )
        ),
        title='3D Bar Chart of Community Overlaps'
    )

    # Save the plot to a file with the current date and time
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"3d_plot_{current_time}.html"
    fig.write_html(file_name)

    print(current_time + ": Created 3d bar diagram with Plotly")

if False: # matplotlib
    # Create the 3D plot
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')

    # Define the range for the subset
    x_range = 100  # Adjust as needed
    y_range = 500  # Adjust as needed

    # Create the x, y coordinates for the subset
    xpos_subset, ypos_subset = np.meshgrid(np.arange(x_range), np.arange(y_range))
    xpos_subset = xpos_subset.flatten()
    ypos_subset = ypos_subset.flatten()
    zpos_subset = np.zeros_like(xpos_subset)

    # Select the counts for the subset and then flatten
    counts_subset = counts[:y_range, :x_range].flatten()

    # Filter out zero values from the subset
    non_zero_indices_subset = counts_subset != 0
    xpos_filtered = xpos_subset[non_zero_indices_subset]
    ypos_filtered = ypos_subset[non_zero_indices_subset]
    zpos_filtered = zpos_subset[non_zero_indices_subset]

    # Create the dx, dy, dz for bar sizes for the filtered subset
    dx_filtered = dy_filtered = np.ones_like(zpos_filtered)
    dz_filtered = counts_subset[non_zero_indices_subset]

    ax.set_zscale('log')
    ax.set_zlim(1, max(dz_filtered))

    ax.bar3d(xpos_filtered, ypos_filtered, zpos_filtered, dx_filtered, dy_filtered, dz_filtered)

    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    print(current_time + ": Created 3d bar diagram")

    ax.set_xlabel('Size of Overlap')
    ax.set_ylabel('Size of Community')
    ax.set_zlabel('Number of Overlaps')

    # Save the plot to a file with the current date and time
    current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"3d_plot_{current_time}.png"
    plt.savefig(file_name)