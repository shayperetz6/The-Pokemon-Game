import random
import time
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *
from client_python.DiGraph import DiGraph
from client_python.algo_stuff import AlgoStuff

class GuiStuff:

    # init pygame
    WIDTH, HEIGHT = 1080, 720
    radius = 15
    pokemons = None
    agents = None
    algo_s: AlgoStuff = None

    """
    the constructor of the class 
    client is client tom connect to using the client class, 
    net graph is a di graph, 
    graph info is a graph in raw form as given from the client
    info is the game info
    """
    def __init__(self, client, net_graph: DiGraph(), graph_info, info):
        self.client = client
        self.my_graph = net_graph
        self.graph = graph_info
        self.game_info = info
        pygame.init()
        self.FONT = pygame.font.SysFont('Arial', 20, bold=True)

        self.screen = display.set_mode((self.WIDTH, self.HEIGHT), depth=32, flags=RESIZABLE)
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.set_graph_bounds()

    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen

    # decorate scale with the correct values

    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height() - 50, self.min_y, self.max_y)

    """
    getting the min and max values of the of the graph
    """
    def set_graph_bounds(self):
        self.min_x = min(list(self.graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.min_y = min(list(self.graph.Nodes), key=lambda n: n.pos.y).pos.y
        self.max_x = max(list(self.graph.Nodes), key=lambda n: n.pos.x).pos.x
        self.max_y = max(list(self.graph.Nodes), key=lambda n: n.pos.y).pos.y


    def start_of_game(self):
        """
        handeling the start sequence , dr oak and start screen
        :return:
        """
        running = True
        bg = pygame.image.load("imges/bg.png")
        bg = pygame.transform.scale(bg, (self.WIDTH, self.HEIGHT))
        self.screen.blit(bg, (0, 0))
        display.update()
        time.wait(2000)

        bg = pygame.image.load("imges/p_oak.png")
        open_word = "Welcome To The World Of Object Oriented Pokemon! press enter to start...."
        bg = pygame.transform.scale(bg, (self.WIDTH, self.HEIGHT))
        self.screen.blit(bg, (0, 0))
        display.update()
        runner = 0
        x = 100
        y = self.screen.get_height() - 130
        for i in range(0,len(open_word)):
            id_srf = self.FONT.render(open_word[0:i], True, Color(0, 0, 0))

            self.screen.blit(id_srf, (x, y))
            display.update()
            time.wait(20)
        please_run = True
        while please_run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.stop()
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        please_run = False
            self.clock.tick(10)


    def game_loop(self):
        """
        game loop -
        handels new data and drawing to the screen
        calls the algo calss the know where to put the agents

        :return:
        """
        start_time = self.client.time_to_end()
        while self.client.is_running() == 'true':
            pokemons = json.loads(self.client.get_pokemons(),
                                  object_hook=lambda d: SimpleNamespace(**d)).Pokemons
            pokemons = [p.Pokemon for p in pokemons]
            for p in pokemons:
                p.src_node = -1
                x, y, _ = p.pos.split(',')
                p.pos = SimpleNamespace(x=self.my_scale(float(x), x=True), y=self.my_scale(float(y), y=True))
                self.algo_s.calc_src_node(p)

            agents = json.loads(self.client.get_agents(),
                                object_hook=lambda d: SimpleNamespace(**d)).Agents
            agents = [agent.Agent for agent in agents]
            for a in agents:
                x, y, _ = a.pos.split(',')
                a.pos = SimpleNamespace(x=self.my_scale(
                    float(x), x=True), y=self.my_scale(float(y), y=True))
            # check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if 35 >= pos[0] >= 5:
                        if 60 >= pos[1] >= 30:
                            self.client.stop()
                            pygame.quit()
                            exit(0)



            # refresh surface
            bg = pygame.image.load("imges/img.png")
            bg = pygame.transform.scale(bg, (self.screen.get_width(), self.screen.get_height()))
            self.screen.blit(bg, (0, 0))

            for e in self.graph.Edges:
                # find the edge nodes
                src = next(n for n in self.graph.Nodes if n.id == e.src)
                dest = next(n for n in self.graph.Nodes if n.id == e.dest)

                # scaled positions
                src_x = self.my_scale(src.pos.x, x=True)
                src_y = self.my_scale(src.pos.y, y=True)
                dest_x = self.my_scale(dest.pos.x, x=True)
                dest_y = self.my_scale(dest.pos.y, y=True)

                # draw the line
                pygame.draw.line(self.screen, Color(0, 0, 0),
                                 (src_x, src_y), (dest_x, dest_y))
                pygame.draw.line(self.screen, Color(0, 0, 0),
                                 (src_x, src_y), (dest_x, dest_y))
            # draw nodes
            for n in self.graph.Nodes:
                x = self.my_scale(n.pos.x, x=True)
                y = self.my_scale(n.pos.y, y=True)

                node_place = pygame.image.load("imges/pokecenter.png")
                node_place = pygame.transform.scale(node_place, (33, 33))
                rect = node_place.get_rect(center=(x, y))
                self.screen.blit(node_place, rect)

                # draw the node id
                id_srf = self.FONT.render(str(n.id), True, Color(255, 255, 255))
                rect = id_srf.get_rect(center=(x, y-13))
                self.screen.blit(id_srf, rect)


            # draw agents
            for agent in agents:
                agent_p = pygame.image.load("imges/agent.png")
                agent_p = pygame.transform.scale(agent_p, (24, 32))
                rect = agent_p.get_rect(center=(int(agent.pos.x), int(agent.pos.y)))
                self.screen.blit(agent_p, rect)

            # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
            for p in pokemons:
                index = p.value*p.type % 16 + 1
                p_p = pygame.image.load("imges/pokemons/p_"+str(int(index))+".png")
                p_p = pygame.transform.scale(p_p, (44, 44))
                rect = p_p.get_rect(center=(int(p.pos.x), int(p.pos.y)))
                if p.type < 0:
                    pygame.draw.circle(self.screen, Color(255, 255, 0), (int(p.pos.x), int(p.pos.y + 20)), 10)
                else:
                    pygame.draw.circle(self.screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y + 20)), 10)
                self.screen.blit(p_p, rect)
            # update screen changes
            display.update()

            self.algo_s.agents = agents
            self.algo_s.pokemons = pokemons

            run_move = self.algo_s.next_node2()
            self.client.move()
            ttl = self.client.time_to_end()
            info = json.loads(self.client.get_info(),
                              object_hook=lambda d: SimpleNamespace(**d)).GameServer

            id_srf = self.FONT.render("TIME: "+str(int(ttl)/1000)+"  Points: "+str(info.grade)+" Moves " +
                                      str(info.moves), True, Color(0, 0, 0))
            self.screen.blit(id_srf, (0, 5))
            pygame.draw.circle(self.screen, Color(255, 255, 255), (int(20), int(45)), 17)
            pygame.draw.circle(self.screen, Color(255, 0, 0), (int(20), int(45)), 15)

            id_srf = self.FONT.render("S", True, Color(255, 255, 255))
            self.screen.blit(id_srf, (14, 32))
            display.update()
# refresh rat
            self.clock.tick(10)
            if int(ttl) <= 100:
                self.client.stop()
                return True



