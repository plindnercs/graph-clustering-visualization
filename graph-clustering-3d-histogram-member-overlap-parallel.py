with open(r'ig_communities_output_120h.metis', 'r') as fp:
    file = fp.readlines()

# create 4-tupel for every community
# ( community id | number of members | size of overlap | members of community as set )
communities = {k: [k, len(file[k].replace('\n', '').split(' ')), 0, set(file[k].replace('\n', '').split(' '))] for k in range(0, len(file))}

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
                if not ((members[member][i], members[member][j]) in pairs_to_compare or (members[member][j], members[member][i]) in pairs_to_compare):
                    pairs_to_compare.add((members[member][i], members[member][j]))

print(len(pairs_to_compare))

# write pairs to a file
with open('pairs_to_compare', 'w') as file:
    for pair in pairs_to_compare:
        print(f"{pair[0]},{pair[1]}\n")
        # file.write(f"{pair[0]},{pair[1]}\n")

# compare pairs and create output
compared_pairs = list()
for pair in pairs_to_compare:
    overlap = len(set.intersection(communities[pair[0]][3], communities[pair[1]][3]))
    if overlap > 0:
        print(overlap)
    compared_pairs.append((pair, overlap))

print(compared_pairs[0])