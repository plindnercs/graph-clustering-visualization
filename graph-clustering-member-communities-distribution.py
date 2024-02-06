import math
import plotly.express as px
from datetime import datetime
#f(i) wie viele Knoten sind in i Communities vorhanden

#1) berechne Anzahl Communities für jeden Knoten
#2) Berechne maximale Anzahl an Communities für jeweils einen Knoten über alle Knoten
#3) für i \in {1, ..., maxAnzahl} Array erstellen und jeweils über alle Knoten drüber und Wert in Array inkrementieren wenn Anzahl Communities = i
#4) i auf x-Achse
#5) f(i) auf y-Achse

with open(r'ig_communities_output_120h.metis', 'r') as fp:
    file = fp.readlines()

# create 4-tupel for every community
# ( community id | number of members | size of overlap | members of community as set )
communities = {k: [k, len(file[k].replace('\n', '').split(' ')), 0, list(file[k].replace('\n', '').split(' '))] for k in range(0, len(file))}

print("number of communities: " + str(len(communities)))

set_of_members = set()
number_of_members = 0
for i in range(0, len(communities)):
    for j in range(0, len(communities[i][3])):
        if not communities[i][3][j] in set_of_members:
            set_of_members.add(communities[i][3][j])
            number_of_members += 1

# the number of members is much lower than in the initial file (members = users), since we leave out all communities
# that are smaller than three during the clustering process
print("number of members: " + str(number_of_members))

# create dict of communities for each member
members = {}
for i in range(0, len(communities)):
    for member in communities[i][3]:
        if int(member) not in members:
            members[int(member)] = 0

        members[int(member)] += 1

#print("number of members: " + str(len(members)))
min_memberships = math.inf
max_memberships = 0
for member in members:
    if members[member] > max_memberships:
        max_memberships = members[member]

    if members[member] < min_memberships:
        min_memberships = members[member]
print("min: " + str(min_memberships))
print("max: " + str(max_memberships))

f_i = [0] * (max_memberships + 1)

for member in members:
    for i in range(0, max_memberships + 1):
        if members[member] == i:
            f_i[i] += 1

print("length f_i: " + str(len(f_i)))
print("f_i(3) = " + str(f_i[3]))

print("sum of f_i(i) for all i: " + str(sum(f_i)))

# Generate the x and y values for the plot
x_values = range(0, max_memberships + 1)
y_values = f_i

# Create the plot using Plotly
fig = px.line(x=x_values, y=y_values, labels={'x':'Number of Communities (i)', 'y':'Number of Nodes in i Communities (f(i))'},
              title='Number of Nodes in i Communities')

# Apply log scaling to the y-axis
fig.update_layout(yaxis_type="log")

# Generate a unique timestamp for the filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"plot_{timestamp}.html"

# Save the figure to an HTML file
fig.write_html(filename)

# Output the filename for reference
print("Plot saved as:", filename)