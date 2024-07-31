# creates a list of all required community overlaps formatted as: community1_id, community2_id, overlap_size
# usage: python3 graph-clustering-3d-histogram-member-overlap-parallel.py ig_communities_output_120h.metis

import sys
from datetime import datetime

file_input = sys.argv[1]

with open(file_input, 'r') as fp:
    file = fp.readlines()

# create 4-tupel for every community
# ( community id | number of members | size of overlap | members of community as set )
communities = {k: [k, len(file[k].replace('\n', '').split(' ')), 0, set(file[k].replace('\n', '').split(' '))] for k in
               range(0, len(file))}

# create list of communities for each member
members = {}

for i in range(0, len(communities)):
    for member in communities[i][3]:
        if int(member) not in members:
            members[int(member)] = list()

        members[int(member)].append(communities[i][0])

# print(len(members[1]))

# create pairs to be compared
pairs_to_compare = set()

for member in members.keys():
    for i in range(0, len(members[member])):
        for j in range(i, len(members[member])):
            if not (members[member][i] == members[member][j]):
                if not ((members[member][i], members[member][j]) in pairs_to_compare or
                        (members[member][j], members[member][i]) in pairs_to_compare):
                    pairs_to_compare.add((members[member][i], members[member][j]))

print(len(pairs_to_compare))

# write pairs to a file
current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# compare pairs and create output
compared_pairs = list()
for pair in pairs_to_compare:
    overlap = len(set.intersection(communities[pair[0]][3], communities[pair[1]][3]))
    # if overlap > 0:
    # print(overlap)
    compared_pairs.append((pair, overlap))

# print(compared_pairs[0])

current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

with open('pairs_to_compare_' + current_time, 'w') as file:
    file.write(str(len(pairs_to_compare)) + '\n')
    for compared_pair in compared_pairs:
        print(f"{compared_pair[0][0]},{compared_pair[0][1]},{compared_pair[1]}")
        file.write(f"{compared_pair[0][0]},{compared_pair[0][1]},{compared_pair[1]}\n")

