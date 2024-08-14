# script to generate a file with random communities with members and a certain overlap
# usage: python3 graph-clustering-generate-random-communities.py <num_members> <num_communities> <max_members_per_community>

import random
import sys
import time

def create_communities(num_members, num_communities, max_members_per_community):
    members = list(range(1, num_members + 1))
    communities = []

    for _ in range(num_communities):
        community_size = random.randint(2, max_members_per_community)
        community = random.sample(members, community_size)
        communities.append(community)

    # Ensure some members appear in multiple communities
    # members_in_multiple_communities = random.sample(members, num_members // 2)
    # for member in members_in_multiple_communities:
    #     chosen_communities = random.sample(communities, random.randint(2, 4))
    #     for community in chosen_communities:
    #         if member not in community:
    #             community.append(member)

    return communities

def save_communities_to_file(communities):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"communities_{timestamp}.txt"

    with open(filename, 'w') as file:
        for community in communities:
            file.write(" ".join(map(str, community)) + "\n")

    print(f"Communities saved to {filename}")


if len(sys.argv) == 4:
    num_members = int(sys.argv[1])
    num_communities = int(sys.argv[2])
    max_members_per_community = int(sys.argv[3])

    # Create and save communities
    communities = create_communities(num_members, num_communities, max_members_per_community)
    save_communities_to_file(communities)
else:
    print("Invalid parameters given, please check documentation!")