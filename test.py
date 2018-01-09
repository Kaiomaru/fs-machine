import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image
import os
from networkx.drawing.nx_agraph import write_dot

G = nx.MultiDiGraph()
G.add_edge(1,1, weight='a', label="a")
G.add_edge(1,1, weight='b', label="b")
G.add_edge(1,2, weight='c', label='c')
print(G.edges())
write_dot(G,'graph.dot')

os.system('dot -Tpng graph.dot > graph.png')

img = Image.open('graph.png')
img = img.resize((int(img.size[0]*1.3), int(img.size[1]*1.3)), Image.ANTIALIAS)
img.save('graph.png')
