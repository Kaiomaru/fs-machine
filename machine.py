#!/usr/bin/python3
# -*- coding: utf-8 -*-

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import os
from PIL import Image

class Machine:

    def __init__(self, dict_=None, startState=None, endStates=None):

        self.graph = nx.MultiDiGraph()

        if not startState:
            return

        self.graph.add_node(startState, style="dashed")
        for end in endStates:
            self.graph.add_node(end, style="filled")

        for key in dict_.keys():
            if key not in self.graph.nodes():
                self.graph.add_node(key)
            for symb in dict_[key]:
                self.graph.add_edge(key, dict_[key][symb], weight=symb, label=symb)

        self.startState = startState
        self.endStates = endStates
        self.dict = dict_
    
    
    def draw(self, filename):
        write_dot(self.graph, "graph.dot")

        os.system("dot -Tpng graph.dot > {}".format(filename))

        img = Image.open(filename)
        img = img.resize((int(img.size[0] * 1.3), int(img.size[1] * 1.3)), Image.ANTIALIAS) #Увеличиваем изображение
        img.save(filename)

    def checkWord(self, word):
        symbs = list(word)
        count = 0
        try:
            currentState = self.startState

            for symb in symbs:
                dict_ = self.dict[currentState]
                if symb in dict_.keys():
                    edges = self.graph[currentState][dict_[symb]]
                    for edge in edges.values():
                        if edge['label'] == symb:
                            edge['color'] = 'blue'
                            self.draw("{}.png".format(count))
                            edge['color'] = 'black'
                    currentState = dict_[symb]
                else:
                    return False, count
                count += 1

            if currentState not in self.endStates:
                return False, count

            return True, count

        except AttributeError as e:
            print(e)
            return False

