import networkx as nx
import matplotlib as mpl

# Task 1.1

G = nx.karate_club_graph()

name, nodes, edges = G.name, G.number_of_nodes(), G.number_of_edges()
print(f'{name} has {nodes} nodes & {edges} edges.')

print('')

print('--- NODES ---')
print('All nodes: ', list(G.nodes))
print('List of nodes with attribute:', nx.get_node_attributes(G, 'club'))
print('Node data:', G.nodes.data())

print('\n')
print('--- EDGES ---')
print('All edges: ', list(G.edges))
print('List of edges with attribute:', nx.get_edge_attributes(G, 'club'))
print('Edge data: ', G.edges.data())

print('')

# Task 1.2

color_map = []
node_dict = nx.get_node_attributes(G, 'club')

# nx.get_node_attributes returns a dict, so I iterate the values of the dict
for value in node_dict.values():
    # if value equals 'Mr. Hi' append a blue node
    if value == 'Mr. Hi':
        color_map.append('blue')
    # else if value equals 'Officer' append a blue node
    elif value == 'Officer':
        color_map.append('green')
    # else if value is anything else append a gray node
    else:
        color_map.append('gray')

# draw the graph, since the colors where applied in the same order as the nodes are ordered
# the correct color will be applied to the corresponding node
nx.draw(G, node_color=color_map, with_labels=True)

# Task 1.3

shortest_path = nx.dijkstra_path(G, 24, 16)
print('Shortest path is:', shortest_path)

# Task 1.4

# nx.get_node_attributes returns a dict, so I iterate the keys of the dict
for value in node_dict.keys():
    # if the key is one of the values in shortest_path it will override that nodes color to red
    if shortest_path.__contains__(value):
        color_map[value] = 'red'

# draw the graph, since the colors where applied in the same order as the nodes are ordered
# the correct color will be applied to the corresponding node
nx.draw(G, node_color=color_map, with_labels=True)
