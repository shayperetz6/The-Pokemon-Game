from random import randrange
from client_python.GraphInterface import GraphInterface


class Node:
    x = 0
    y = 0
    z = 0
    ID = 0
    out_num = 0
    in_num = 0
    tag = 0
    tag2 = False
    prev = 0

    def __init__(self, x, y, z, id1):
        self.x = x
        self.y = y
        self.z = z
        self.ID = id1

    def __repr__(self):
        return "" + str(self.ID) + ": |edges_out| " + str(self.out_num) + " |edges_in| " + str(self.in_num)


class DiGraph(GraphInterface):
    v_num = 0
    e_num = 0
    """
    {id: (Node, {out edges}, {in edges})}
    """
    graph = {-1: [Node, {}, {}]}
    mc = 0

    def __init__(self):
        self.v_num = 0
        self.e_num = 0
        self.graph = {}
        self.mc = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return self.v_num

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.e_num

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        all_v = {}
        for key in self.graph.keys():
            all_v[key] = self.graph[key][0]
        return all_v

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        if id1 not in self.graph.keys():
            return {"key not found": None}
        all_v = {}
        for key in self.graph[id1][2].keys():
            all_v[key] = self.graph[id1][2][key]
        return all_v

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        if id1 not in self.graph.keys():
            return {"key not found": None}
        all_v = {}
        for key in self.graph[id1][1].keys():
            all_v[key] = self.graph[id1][1][key]
        return all_v

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 not in self.graph.keys():
            return False
        if id2 not in self.graph.keys():
            return False
        for edge in self.graph[id1][1]:
            if edge == id2:
                return False
        self.mc += 1
        self.e_num += 1
        self.graph[id1][1][id2] = weight
        self.graph[id1][0].out_num += 1
        self.graph[id2][2][id1] = weight
        self.graph[id2][0].in_num += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        for n_id in self.graph.keys():
            if n_id == node_id:
                return False

        my_node = Node(randrange(10, 640), randrange(10, 350), randrange(10, 640), node_id)
        if pos is not None:
            my_node = Node(pos[0], pos[1], pos[2], node_id)
        self.mc += 1
        self.v_num += 1
        self.graph[node_id] = [my_node, {}, {}]
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id not in self.graph.keys():
            return False
        out_dict = self.graph[node_id][1]
        for out_id in out_dict.keys():
            if node_id in self.graph[out_id][2]:
                self.graph[out_id][0].in_num -= 1
            self.graph[out_id][2].pop(node_id, None)

        in_dict = self.graph[node_id][2]
        for in_id in in_dict.keys():
            if node_id in self.graph[in_id][1]:
                self.graph[in_id][0].out_num -= 1
            self.graph[in_id][1].pop(node_id, None)

        self.e_num -= self.graph[node_id][0].out_num
        self.e_num -= self.graph[node_id][0].in_num
        self.v_num -= 1
        self.mc += self.graph[node_id][0].out_num
        self.mc += self.graph[node_id][0].in_num
        self.mc += 1
        self.graph.pop(node_id)
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 not in self.graph.keys():
            return False
        if node_id2 not in self.graph.keys():
            return False
        if node_id2 not in self.graph[node_id1][1].keys():
            return False
        self.e_num -= 1
        self.mc += 1
        self.graph[node_id1][1].pop(node_id2, None)
        self.graph[node_id2][2].pop(node_id1, None)
        self.graph[node_id1][0].out_num -= 1
        self.graph[node_id2][0].in_num -= 1
        return True

    def __repr__(self):
        return "Graph: |V|" + str(self.v_num) + " , |E| " + str(self.e_num)