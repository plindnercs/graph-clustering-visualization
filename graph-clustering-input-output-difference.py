# script to compare the original input graph and the output graph
# we want to know if the nodes of the output graph are all a part of the input graph
# additionally, we want to see how the nodes of the original graph are connected to the clustered output graph
# usage: python3 graph-clustering-input-output-difference.py graph1.metis graph2.metis
import sys

original_input_graph = sys.argv[1]
output_graph = sys.argv[2]

nodes_of_input_graph = set()
nodes_of_output_graph = set()

file_lines = 0
with open(original_input_graph, 'r') as file:
    next(file)  # skip the first line
    for line in file:
        file_lines += 1
        # split the line into numbers and add each to the set
        ids = line.split()
        nodes_of_input_graph.update(map(int, ids))  # convert strings to integers and update the set

print("Number of nodes in original input graph: " + str(len(nodes_of_input_graph)))
print("Number of lines in original input graph: " + str(file_lines))

file_lines = 0
with open(output_graph, 'r') as file:
    for line in file:
        file_lines += 1
        # split the line into numbers and add each to the set
        ids = line.split()
        nodes_of_output_graph.update(map(int, ids))  # convert strings to integers and update the set

print("Number of nodes in clustered output graph: " + str(len(nodes_of_output_graph)))
print("Number of lines in clustered output graph: " + str(file_lines))

if nodes_of_output_graph.issubset(nodes_of_input_graph):
    print("Output graph is subset of input graph")

difference_of_graphs = nodes_of_input_graph.difference(nodes_of_output_graph)

print("Size of difference: " + str(len(difference_of_graphs)))