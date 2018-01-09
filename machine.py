#!/usr/bin/python3
# -*- coding: utf-8 -*-

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
from PIL import Image

class Machine:

    def __init__(self, dict, startState, endStates):
        self.graph = nx.DiGraph()
        for key in dict.keys():
            self.graph.add_node(key)
            for symb in dict[key]:
                self.graph.add_edge(key, dict[key][symb], label=symb, weight=symb)
        write_dot(self.graph,'graph.dot')

        os.system('dot -Tpng graph.dot > graph.png')

        img = Image.open('graph.png')
        img = img.resize((int(img.size[0]*1.3), int(img.size[1]*1.3)), Image.ANTIALIAS)
        img.save('graph.png') 