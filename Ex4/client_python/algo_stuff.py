import math as py_math
import time
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.DiGraph import DiGraph
from client_python.GraphAlgo import GraphAlgo


class AlgoStuff:

    pokemons = None
    agents = None
    graph_info = None

    """
        the constructor of the class 
        client is client tom connect to using the client class, 
        graph is a di graph, 
        info is the game info
        """
    def __init__(self, client, graph: DiGraph, info):
        self.client = client
        self.my_graph: DiGraph = graph
        self.game_info = info
        self.agents_path = []
        self.agents_prev = []

    """
    adding agents to the game 
    calc where to put them.
    """
    def add_agents_algo(self):
        if self.client is not None:
            print(int(self.game_info.agents))
            runner = 0
            pk_runner = 0

            while runner < int(self.game_info.agents):
                self.agents_path.append([])
                self.client.add_agent("{\"id\":"+str(int(self.pokemons[pk_runner].src_node))+"}")
                self.agents_prev.append(int(self.pokemons[pk_runner].src_node))
                pk_runner = (pk_runner+1) % len(self.pokemons)
                runner += 1
        else:
            return False

    """
    calc the dist between 2 points
    """
    def dist(self, x1, y1, x2, y2):
        return py_math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

    """
    calc thee src node and dest node of each pokemon, used for the algorithem 
    """
    def calc_src_node(self, pokemon):
        if self.my_graph is None:
            return False
        min_index_src = -1
        min_index_dest = -1
        min_dist = float('inf')
        for node in self.my_graph.get_all_v():
            for dest in self.my_graph.all_out_edges_of_node(node):

                src_x, src_y = self.my_graph.graph[node][0].x, self.my_graph.graph[node][0].y
                dst_x, dst_y = self.my_graph.graph[dest][0].x, self.my_graph.graph[dest][0].y
                p_x, p_y = pokemon.pos.x, pokemon.pos.y
                s_p_d = self.dist(src_x, src_y, p_x, p_y) + self.dist(p_x, p_y, dst_x, dst_y)
                s_d = self.dist(src_x, src_y, dst_x, dst_y)
                if s_p_d-s_d <= min_dist:
                    min_index_src = node
                    min_index_dest = dest
                    min_dist = s_p_d-s_d
        if pokemon.type > 0:
            if min_index_src < min_index_dest:
                pokemon.src_node = min_index_src
                pokemon.dst_node = min_index_dest
            else:
                pokemon.src_node = min_index_dest
                pokemon.dst_node = min_index_src
        if pokemon.type < 0:
            if min_index_src > min_index_dest:
                pokemon.src_node = min_index_src
                pokemon.dst_node = min_index_dest
            else:
                pokemon.src_node = min_index_dest
                pokemon.dst_node = min_index_src

    """
    calc the next node of the agents 
    """
    def next_node2(self):
        if self.client is None or self.my_graph is None:
            return False
        """
        by the social distncing and max value path algo
        try not to colide as much as they can
        but still go to best path
        :return:
        """
        # choose next edge
        algo_graph = GraphAlgo(self.my_graph)
        need_to_move = False

        for agent in self.agents:
            if agent.dest == -1:
                need_to_move = True
                max_worth = 0
                next_visit = agent.src
                keep_check = True
                for pokemon in self.pokemons:
                    if keep_check:
                        if agent.src == pokemon.src_node:
                            keep_check = False
                            next_visit = pokemon.dst_node
                            need_to_move = True
                        else:
                            worth, path = algo_graph.shortest_path(agent.src, pokemon.src_node)
                            """
                            need to change upper part
                            """
                            poke_sum = 1
                            for pokemon in self.pokemons:
                                if pokemon.src_node in path:
                                    poke_sum += pokemon.value
                            worth = (agent.value*agent.value*1000 + poke_sum)/((worth+0.1)*(worth+0.1))

                            for agent2 in self.agents:
                                if path[1] == agent2.dest:
                                    worth = py_math.sqrt(worth)

                            if worth > max_worth:
                                max_worth = worth
                                next_visit = path[1]

                self.client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_visit) + '}')

        return need_to_move



