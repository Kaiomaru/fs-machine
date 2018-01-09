#!/usr/bin/python3
# -*- coding: utf-8 -*-

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
from PIL import Image

class Machine:

    def __init__(self, dict, startState, endStates):
        self.graph = nx.DiGraph()

        self.graph.add_node(startState, style="dashed")
        for end in endStates:
            self.graph.add_node(end, style="filled")

        for key in dict.keys():
            if key not in self.graph.nodes():      #Начальные и конечные состояния уже лежат в нодах графа
                self.graph.add_node(key)
            for symb in dict[key]:
                self.graph.add_edge(key, dict[key][symb], label=symb, weight=symb)

    
    def draw(self, filename):
        write_dot(self.graph, "graph.dot")

        os.system("dot -Tpng graph.dot > {}".format(filename))

        img = Image.open(filename)
        img = img.resize((int(img.size[0] * 1.4), int(img.size[1] * 1.4)), Image.ANTIALIAS) #Увеличиваем изображение в 1.4 раза
        img.save(filename) 