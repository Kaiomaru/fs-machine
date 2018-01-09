import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import os
from networkx.drawing.nx_agraph import write_dot

G = nx.DiGraph()
G.add_edges_from([(0,1), (0,2), (1,1), (1,2), (1,3), (2,4), (1,4), (3,4), (4,5), (4,6), (3,7)])
#G[1][2]['color'] = 'red'
#G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_node(0, color='blue', style='bold')
write_dot(G,'graph.dot')

os.system('dot -Tpng graph.dot > graph.png')

img = Image.open('graph.png')
img = img.resize((int(img.size[0]*1.3), int(img.size[1]*1.3)), Image.ANTIALIAS)
img.save('graph.png') 