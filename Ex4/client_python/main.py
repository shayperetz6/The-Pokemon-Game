"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
import time
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.DiGraph import DiGraph
from client_python.algo_stuff import AlgoStuff
from client_python.gui_stuff import GuiStuff

# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

"""
calls thr scale func with the changed data

"""
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, WIDTH - 50, min_x, max_x)
    if y:
        return scale(data, 50, HEIGHT - 50, min_y, max_y)

"""
the main function that connect to the server and start the game by calling the gui and the algo
the glue of thr class we buillt 
"""
def my_main():
    global min_x
    global min_y
    global  max_x
    global max_y
    client = Client()
    client.start_connection(HOST, PORT)

    graph_json = client.get_graph()

    graph = json.loads(
        graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))
    """
    creats the graph from the data given to us 
    """
    net_graph = DiGraph()
    for n in graph.Nodes:
        x, y, _ = n.pos.split(',')
        n.pos = SimpleNamespace(x=float(x), y=float(y), z=0)

    min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
    min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
    max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
    max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y

    for n in graph.Nodes:
        x = n.pos.x
        y = n.pos.y
        x = my_scale(float(x), x=True)
        y = my_scale(float(y), y=True)
        net_graph.add_node(n.id, (x, y, 0))

    for e in graph.Edges:
        net_graph.add_edge(e.src, e.dest, e.w)

    info = json.loads(client.get_info(),
                        object_hook=lambda d: SimpleNamespace(**d)).GameServer


    print(info)
    print(net_graph)
    algos: AlgoStuff = AlgoStuff(client, net_graph, info)
    algos.graph_info = graph
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
        algos.calc_src_node(p)

    algos.pokemons = pokemons
    algos.add_agents_algo()

    gui = GuiStuff(client, net_graph, graph, info)
    gui.start_of_game()

    client.start()

    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    info = json.loads(client.get_info(),
                        object_hook=lambda d: SimpleNamespace(**d)).GameServer

    algos.pokemons = pokemons
    algos.agents = agents
    print(algos.pokemons)
    print(algos.agents)
    gui = GuiStuff(client, net_graph, graph, info)
    gui.pokemons = pokemons
    gui.algo_s = algos
    gui.agents = agents

    return gui.game_loop()


min_x = 0
min_y = 0
max_x = 0
max_y = 0

if __name__ == '__main__':
    my_main()