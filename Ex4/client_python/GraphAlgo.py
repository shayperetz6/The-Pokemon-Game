import json

from client_python.GraphAlgoInterface import GraphAlgoInterface
from client_python.GraphInterface import GraphInterface
from client_python.DiGraph import DiGraph

from itertools import permutations
from typing import List

from tkinter import *
from tkinter import messagebox

colors = ["LightSkyBlue1", "LightSkyBlue2", "LightSkyBlue3", "LightSkyBlue4"]


class GraphGui:
    my_graph = None

    def __init__(self, master, graph=DiGraph()):
        """
        sets all the GUI in the root we got
        and saves the graph in self.my_graph
        """
        self.my_graph = graph
        global colors
        master.geometry("900x430")
        master.resizable(0, 0)
        base = Frame(master)
        base.grid(row=0, column=0)

        self.up_frame = Frame(base, borderwidth=2, relief=FLAT, background=colors[3], width=901, height=30)
        self.up_frame.grid(row=0, column=0)
        Label(self.up_frame, text="Graph User Interface, read readme.md in github to know how to use", background=colors[3],
              font=("Helvetica", 12), foreground="white").place(x=150)
        self.down_frame = Frame(base, borderwidth=2, relief=RAISED, background=colors[0], width=901, height=401)
        self.down_frame.grid(row=2, column=0)

        self.screen = Canvas(self.down_frame, borderwidth=2, relief=FLAT, background=colors[3], width=650, height=360)
        self.screen.place(x=10, y=10)

        Label(self.down_frame, text="shortest path - format int,int", background=colors[0],
              font=("Helvetica", 10)).place(x=680, y=20)
        self.sp = Entry(self.down_frame, width=30, borderwidth=2, font=("Helvetica", 8, "bold"))
        self.sp.place(x=680, y=40)

        Label(self.down_frame, text="TSP - format int,int,.....,int", background=colors[0],
              font=("Helvetica", 10)).place(x=680, y=60)
        self.tsm = Entry(self.down_frame, width=30, borderwidth=2, font=("Helvetica", 8, "bold"))
        self.tsm.place(x=680, y=80)

        center_b = Button(self.down_frame, text="show center", command=lambda: self.show_center(), borderwidth=1,
                          relief=GROOVE, width=10, background=colors[2])
        center_b.place(x=680, y=110)

        reset_b = Button(self.down_frame, text="reset graph", command=lambda: self.show_graph(), borderwidth=1,
                         relief=GROOVE, width=10, background=colors[2])
        reset_b.place(x=680, y=140)

        self.sp.bind("<Key>", self.focus1)
        self.tsm.bind("<Key>", self.focus2)
        self.show_graph()

    def focus1(self, e):
        """
        'listen' to an entery and wait for enter key to run sp algo
        """
        if e.char == "\r":
            self.run_sp()

    def focus2(self, e):
        """
        'listen' to an entery and wait for enter key to run tsm algo
        """
        if e.char == "\r":
            self.run_tsm()

    def show_center(self):
        """
        coloring the center if exist in a different color
        raising a info message box with the id and dest
        """
        algo = GraphAlgo(self.my_graph)
        center, dist = algo.centerPoint()
        messagebox.showinfo("Information", f"Center id: {center} ,max dist is {dist}")
        if dist != float('inf'):
            v_dict = self.my_graph.get_all_v()
            max_x = 0
            min_x = float('inf')
            max_y = 0
            min_y = float('inf')
            for n in v_dict:
                n = v_dict[n]
                x_val = float(n.x)
                y_val = float(n.y)
                if x_val > max_x:
                    max_x = x_val
                if x_val < min_x:
                    min_x = x_val

                if y_val > max_y:
                    max_y = y_val
                if y_val < min_y:
                    min_y = y_val

            abs_x = abs(min_x - max_x)
            abs_y = abs(min_y - max_y)
            scale_x = 0
            scale_y = 0
            if self.my_graph.v_num == 1:
                scale_x = 1
                scale_y = 1
            else:
                scale_x = 620 / abs_x
                scale_y = 320 / abs_y

            x0_val = float(v_dict[center].x)
            y0_val = float(v_dict[center].y)
            x0_val = abs(x0_val - min_x) * scale_x + 20
            y0_val = abs(y0_val - min_y) * scale_y + 20
            self.screen.create_oval(x0_val - 10, y0_val - 10, x0_val + 10, y0_val + 10, fill='sienna3')

    def run_sp(self):
        """
        running the algo with data we got from the user
        raising an error message box if an error ocuurd with the error diteles
        raising a info message box with the path and dest
        """
        data1 = self.sp.get()
        self.sp.delete(0, 'end')
        data1 = data1.split(",")
        if len(data1) > 2:
            messagebox.showerror("Error", "Oh No Got too much data \n follow the instructions next time!")
            return False
        elif len(data1) == 1:
            messagebox.showerror("Error", "Oh No Not enough data \n follow the instructions next time!")
            return False

        id1: str = data1[0]
        id2: str = data1[1]
        if (not id1.isnumeric()) or (not id2.isnumeric()):
            messagebox.showerror("Error", "data is not integers \n follow the instructions next time!")
            return False
        else:
            id1 = int(id1)
            id2 = int(id2)

        if id1 == id2:
            messagebox.showerror("Error", "id1 equal to id2 \n they need to be different!")
            return False
        algo = GraphAlgo(self.my_graph)
        dist, nodes = algo.shortest_path(id1, id2)
        messagebox.showinfo("Information", f"pathis id: {nodes} \n max dist is {dist}")
        if dist != float('inf'):
            self.colored_lines(nodes)

    def run_tsm(self):
        """
        running the algo with data we got from the user
        raising an error message box if an error ocuurd with the error diteles
        raising a info message box with the path and dest
        """
        data = self.tsm.get()
        self.tsm.delete(0, 'end')
        data = data.split(",")
        if len(data) == 1:
            messagebox.showerror("Error", "Oh No Not enough data \n follow the instructions next time!")
            return False

        for i in range(0, len(data)):
            if not data[i].isnumeric():
                messagebox.showerror("Error", "data is not integers \n follow the instructions next time!")
                return False
            else:
                data[i] = int(data[i])
        algo = GraphAlgo(self.my_graph)

        nodes, dist = algo.TSP(data)
        messagebox.showinfo("Information", f"pathis id: {nodes} \n max dist is {dist}")
        if dist != float('inf'):
            self.colored_lines(nodes)

    def colored_lines(self, nodes_list):
        """
        print the nodes and their connctions to the screen in a diffrent color from the rest of the graph
        :param nodes_list:
        :return:
        """
        self.show_graph()
        v_dict = self.my_graph.get_all_v()
        max_x = 0
        min_x = float('inf')
        max_y = 0
        min_y = float('inf')
        for n in v_dict:
            n = v_dict[n]
            x_val = float(n.x)
            y_val = float(n.y)
            if x_val > max_x:
                max_x = x_val
            if x_val < min_x:
                min_x = x_val

            if y_val > max_y:
                max_y = y_val
            if y_val < min_y:
                min_y = y_val

        abs_x = abs(min_x - max_x)
        abs_y = abs(min_y - max_y)
        scale_x = 0
        scale_y = 0
        if self.my_graph.v_num == 1:
            scale_x = 1
            scale_y = 1
        else:
            scale_x = 620 / abs_x
            scale_y = 320 / abs_y
        for n in range(0, len(nodes_list)):
            curr_id = nodes_list[n]
            x0_val = float(v_dict[curr_id].x)
            y0_val = float(v_dict[curr_id].y)
            x0_val = abs(x0_val - min_x) * scale_x + 20
            y0_val = abs(y0_val - min_y) * scale_y + 20
            if n == 0:
                self.screen.create_oval(x0_val - 10, y0_val - 10, x0_val + 10, y0_val + 10, fill='yellow')
            elif n == len(nodes_list)-1:
                self.screen.create_oval(x0_val - 10, y0_val - 10, x0_val + 10, y0_val + 10, fill='yellow')
            else:
                self.screen.create_oval(x0_val - 10, y0_val - 10, x0_val + 10, y0_val + 10, fill='LightSkyBlue3')
        for n in range(0, len(nodes_list)-1):
            curr_id = nodes_list[n]
            next_id = nodes_list[n+1]
            edge = v_dict[next_id]
            x0_val = float(v_dict[curr_id].x)
            y0_val = float(v_dict[curr_id].y)
            x0_val = abs(x0_val - min_x) * scale_x + 20
            y0_val = abs(y0_val - min_y) * scale_y + 20
            x1_val = float(edge.x)
            y1_val = float(edge.y)
            x1_val = abs(x1_val - min_x) * scale_x + 20
            y1_val = abs(y1_val - min_y) * scale_y + 20
            self.screen.create_line(x0_val, y0_val, x1_val, y1_val, arrow=LAST, width=2, fill="green")

    def show_graph(self):
        """
        print the graph to the screen
        :return:
        """
        v_dict = self.my_graph.get_all_v()
        max_x = 0
        min_x = float('inf')
        max_y = 0
        min_y = float('inf')
        for n in v_dict:
            n = v_dict[n]
            x_val = float(n.x)
            y_val = float(n.y)
            if x_val > max_x:
                max_x = x_val
            if x_val < min_x:
                min_x = x_val

            if y_val > max_y:
                max_y = y_val
            if y_val < min_y:
                min_y = y_val

        abs_x = abs(min_x - max_x)
        abs_y = abs(min_y - max_y)
        scale_x = 0
        scale_y = 0
        if self.my_graph.v_num == 1:
            scale_x = 1
            scale_y = 1
        else:
            scale_x = 620/abs_x
            scale_y = 320/abs_y

        for n in v_dict:
            curr_id = n
            n = v_dict[n]

            x_val = float(n.x)
            y_val = float(n.y)

            x_val = abs(x_val-min_x)*scale_x+20
            y_val = abs(y_val - min_y)*scale_y+20
            self.screen.create_text(x_val, y_val+20, text=str(curr_id), fill="black", font='Helvetica 11 bold')
            self.screen.create_oval(x_val-10, y_val-10, x_val+10, y_val+10, fill='white')

        for n in v_dict:
            curr_id = n
            n = v_dict[n]
            for edge in self.my_graph.all_out_edges_of_node(curr_id):
                edge = v_dict[edge]
                x0_val = float(n.x)
                y0_val = float(n.y)
                x0_val = abs(x0_val - min_x)*scale_x+20
                y0_val = abs(y0_val - min_y)*scale_y+20
                x1_val = float(edge.x)
                y1_val = float(edge.y)
                x1_val = abs(x1_val - min_x)*scale_x+20
                y1_val = abs(y1_val - min_y)*scale_y+20
                self.screen.create_line(x0_val, y0_val, x1_val, y1_val, arrow=LAST, width=2)


class GraphAlgo(GraphAlgoInterface):
    my_graph = DiGraph()

    def __init__(self, g=DiGraph()):
        self.my_graph = g

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.my_graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        self.my_graph = DiGraph()
        f = 0

        f = open(file_name)
        data: dict = json.load(f)
        try:
            for node in data['Nodes']:
                if 'pos' in node.keys():
                    pos = str(node['pos'])
                    pos = pos.split(",")
                    pos = pos[0], pos[1], pos[2]
                    self.my_graph.add_node(node['id'], pos)
                self.my_graph.add_node(node['id'])
            for edge in data['Edges']:
                self.my_graph.add_edge(edge['src'], edge['dest'], edge['w'])
            f.close()
        except:
            f.close()
            return False

        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        f = 0
        try:
            f = open(file_name, "w")
            datas = {}
            datas['Edges'] = []
            for n_id in self.my_graph.get_all_v().keys():
                out_dict = self.my_graph.all_out_edges_of_node(n_id)
                for dest_id in out_dict.keys():
                    datas['Edges'].append({"src": n_id, "w": out_dict[dest_id], "dest": dest_id})
            datas['Nodes'] = []
            node_dict = self.my_graph.get_all_v()
            for n_id in node_dict.keys():
                datas['Nodes'].append({"pos": str(node_dict[n_id].x)+","+str(node_dict[n_id].y)+","+str(node_dict[n_id].z)
                                      , "id": n_id})
            json.dump(datas, f)
            f.close()
        except:
            return False

        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        if id1 not in self.my_graph.graph.keys():
            return float('inf'), []
        if id2 not in self.my_graph.graph.keys():
            return float('inf'), []

        self.set_tag(float('inf'))
        self.set_tag2(False)
        self.set_prev()
        path_set = {}
        for node in self.my_graph.get_all_v().values():
            path_set[node.ID] = node

        path_set[id1].tag = 0
        path_set[id1].tag2 = True
        done = 0
        min_node = id1
        while done < self.my_graph.v_size():
            done += 1
            curr = path_set[min_node]
            curr.tag2 = True
            if curr is not None:
                for e in self.my_graph.all_out_edges_of_node(min_node):
                    if curr.tag + self.my_graph.all_out_edges_of_node(min_node)[e] < path_set[e].tag:
                        path_set[e].tag = curr.tag + self.my_graph.all_out_edges_of_node(min_node)[e]
                        path_set[e].prev = curr.ID
            min_w = float('inf')
            for key in path_set:
                if path_set[key].tag2 is False:
                    if path_set[key].tag < min_w:
                        min_w = path_set[key].tag
                        min_node = path_set[key].ID

        if path_set[id2].tag != float('inf'):
            path = [id2]
            curr = id2
            while curr != id1:
                curr = path_set[curr].prev
                path.append(curr)
            path.reverse()

            return path_set[id2].tag, path
        return float('inf'), []

    def set_tag(self, data):
        """
        set tha tag of all node to data
        :param data: what data to set
        """

        for node in self.my_graph.get_all_v().values():
            node.tag = data

    def set_tag2(self, data):
        """
        set tha tag2 of all node to data
        :param data: what data to set
        """
        for node in self.my_graph.get_all_v().values():
            node.tag2 = data

    def set_prev(self):
        """
        set prev of all node nodes to node it self
        :return:
        """
        for node in self.my_graph.get_all_v().values():
            node.prev = node.ID

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        for i in node_lst:
            if self.my_graph.get_all_v().get(i, None) is None:
                return [], float('inf')

        curr = self.my_graph
        v = curr.v_size()
        runner = 0
        translate_to_met = {}
        translate_to_graph = {}
        for node in self.my_graph.get_all_v().values():
            translate_to_met[runner] = node.ID
            runner += 1

        runner = 0
        for node in self.my_graph.get_all_v().values():
            translate_to_graph[node.ID] = runner
            runner += 1
        adj_mat = []

        for i in range(0, v):
            adj_mat.append([])
            for j in range(0, v):
                adj_mat[i].append([[], float('inf')])
        for i in range(0, v):
            adj_mat[i][i] = [[], 0]

        for i in range(0, v):
            out_e = self.my_graph.all_out_edges_of_node(translate_to_met[i])
            for con in out_e.keys():
                adj_mat[i][translate_to_graph[con]][1] = out_e[con]

        for a in range(0, v):
            for b in range(0, v):
                for c in range(0, v):
                    if adj_mat[b][c][1] > adj_mat[b][a][1] + adj_mat[a][c][1]:
                        adj_mat[b][c][1] = adj_mat[b][a][1] + adj_mat[a][c][1]
                        adj_mat[b][c][0] = []
                        for i in adj_mat[b][a][0]:
                            adj_mat[b][c][0].append(i)
                        adj_mat[b][c][0].append(a)
                        for i in adj_mat[a][c][0]:
                            adj_mat[b][c][0].append(i)

        tsp_g = DiGraph()
        for num in node_lst:
            tsp_g.add_node(num)
        for src in node_lst:
            for dest in node_lst:
                if src != dest:
                    tsp_g.add_edge(src, dest, adj_mat[src][dest][1])
        min_way_index = 0
        min_ways = []
        runner = 0
        all_ways = list(permutations(node_lst))
        for way in all_ways:
            path = 0
            temp = node_lst.copy()
            for start in range(0, len(way)-1):
                if way[start+1] in temp:
                    path += adj_mat[way[start]][way[start+1]][1]
                    list_to_pop = []
                    for i in temp:
                        if i in adj_mat[way[start]][way[start+1]][0]:
                            list_to_pop.append(i)
                    for j in list_to_pop:
                        if j in temp:
                            temp.remove(j)
            min_ways.append(path)
            if min_ways[min_way_index] > path:
                min_way_index = runner
            runner += 1
        traveling_plan = []
        way = all_ways[min_way_index]
        for start in range(0, len(way)-1):
            path = adj_mat[way[start]][way[start + 1]][0]
            traveling_plan.append(way[start])
            for p in path:
                traveling_plan.append(p)

        traveling_plan.append(way[len(way)-1])
        return traveling_plan, min_ways[min_way_index]

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        curr = self.my_graph
        v = curr.v_size()
        runner = 0
        translate_to_met = {}
        translate_to_graph = {}
        for node in self.my_graph.get_all_v().values():
            translate_to_met[runner] = node.ID
            runner += 1

        runner = 0
        for node in self.my_graph.get_all_v().values():
            translate_to_graph[node.ID] = runner
            runner += 1
        adj_mat = []

        for i in range(0, v):
            adj_mat.append([])
            for j in range(0, v):
                adj_mat[i].append(float('inf'))
        for i in range(0, v):
            adj_mat[i][i] = 0

        for i in range(0, v):
            out_e = self.my_graph.all_out_edges_of_node(translate_to_met[i])
            for con in out_e.keys():
                adj_mat[i][translate_to_graph[con]] = out_e[con]

        for a in range(0, v):
            for b in range(0, v):
                for c in range(0, v):
                    if adj_mat[b][c] > adj_mat[b][a] + adj_mat[a][c]:
                        adj_mat[b][c] = adj_mat[b][a] + adj_mat[a][c]

        max_dist = []
        for i in range(0, v):
            max_d = float('inf')*-1
            for j in range(0, v):
                if adj_mat[i][j] > max_d:
                    max_d = adj_mat[i][j]
            max_dist.append(max_d)
        center = 0
        for i in range(0, v):
            if max_dist[i] == float('inf'):
                return None, float('inf')
            if max_dist[center] > max_dist[i]:
                center = i
        return translate_to_met[center], max_dist[center]

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        root = Tk()
        root.wm_title('G.G-oop ex3')
        GraphGui(root, self.my_graph)
        root.mainloop()
