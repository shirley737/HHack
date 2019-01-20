
'''
Agent construction. Determines what moves to make dependent on state of
gameboard.
'''


from __future__ import print_function
# from heapq import *
import heapq
import logging
import numpy as np
import sys

logging.basicConfig(
        format="%(asctime)s [%(threadName)s][%(levelname)-5.5s][%(module)s:%(funcName)s:%(lineno)d] %(message)s",
        level=logging.INFO)

ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]
HEURISTIC_CONST = 30

class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)

    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        self.final_cost = None
        if self.type == "bfs":
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "astar":
            self.costs = np.ones((self.grid.row_range, self.grid.col_range)) * sys.maxsize
            self.frontier = [(self.dist(self.start, self.goal), self.start)]
            self.explored = []

    def show_result(self):
        current = self.goal
        commands = []
        while not current == self.start:
            command = self.find_action(self.previous[current], current)
            print(command)
            current = self.previous[current]
            self.grid.nodes[current].in_path = True #This turns the color of the node to red
        if self.final_cost is not None:
            print("final cost:", self.final_cost)
        print(" --- ")
        self.grid.start = self.goal

    def find_action(self, s_node, e_node):
        x_dir = e_node[0] - s_node[0]
        y_dir = e_node[1] - s_node[1]
        return (x_dir, y_dir)

    def make_step(self):
        if self.type == "bfs":
            self.bfs_step()
        elif self.type == "astar":
            self.astar_step()

    def dist(self, node_1, node_2):
# XXX: Euclidean distance
#        x2 = (node_1[0] - node_2[0])**2
#        y2 = (node_1[1] - node_2[1])**2
#        return float(np.sqrt(x2 + y2)) * HEURISTIC_CONST
        # Manhattan distance.
        x2 = np.abs(node_1[0] - node_2[0])
        y2 = np.abs(node_1[1] - node_2[1])
        return (np.sqrt(x2 + y2)) * HEURISTIC_CONST

    def bfs_step(self):
        logging.debug("Enter bfs_step")
        # Make sure frontier is not empty.
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        logging.debug("current node: ", current)
        # Perfrom housekeeping procedures; mark as visited; set not in frontier
        # list; and save path (nodes) during exploration.
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        # Check though all children nodes to determine which direction we should
        # explore next. Make sure to not explore nodes we have already explored.
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                logging.debug("explored before: ", node)
                continue
            # Make sure the node is a valid node wrt map dimension.
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                # If this node is a aisle, report and do nothing.
                if self.grid.nodes[node].aisle:
                    logging.debug("aisle at: ", node)
                else:
                    # Record the parent node, and check if we are done.
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        # Insert this node to beginning of queue.
                        self.frontier.insert(0, node)
                        # Indicate this node in currently in the stack.
                        self.grid.nodes[node].frontier = True
            else:
                logging.debug("out of range: ", node)


    def astar_step(self):
        # Initialize some helper variables to keep track of cost, and last node.
        logging.debug("Enter ucs_step")
        # Make sure frontier is not empty.
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        curr_cost, current = heapq.heappop(self.frontier)
        curr_cost -= self.dist(current, self.goal) # Get the actual cost value.
        logging.debug("curr_cost {}".format(curr_cost))
        logging.debug("current node: ", current)
        # Perfrom housekeeping procedures; mark as visited; set not in frontier
        # list; and save path (nodes) during exploration.
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        # Check though all children nodes to determine which direction we should
        # explore next. Make sure to not explore nodes we have already explored.
        for node in children:
            #logging.debug("self.frontier {}".format(self.frontier))
            #See what happens if you disable this check here
            if node in self.explored:
                logging.debug("explored before: ", node)
                continue
            # Make sure the node is a valid node wrt map dimension.
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                # If this node is a aisle, report and do nothing.
                if self.grid.nodes[node].aisle:
                    logging.debug("aisle at: ", node)
                else:
                    # Determine the hueristic cost.
                    cost = self.grid.nodes[node].cost() + curr_cost + self.dist(node, self.goal)
                    logging.debug("node.cost() {}".format(cost))
                    if node == self.goal:
                        self.previous[self.goal] = current
                        self.final_cost = cost
                        self.finished = True
                        return
                    elif cost <= self.costs[node]:
                        exists = False
                        self.previous[node] = current
                        # Insert this node into priority queue.
                        for i, x in enumerate(self.frontier):
                            # If this is the same node, we will replace in queue.
                            if x[1] == node:
                                self.frontier[i] = (cost, node)
                                self.costs[node] = cost
                                heapq.heapify(self.frontier) # Resort heap.
                                exists = True
                        # Node's first time in frontier.
                        if not exists:
                            heapq.heappush(self.frontier, (cost, node))
                        # Indicate this node in currently in the stack.
                        self.grid.nodes[node].frontier = True
            else:
                logging.debug("out of range: ", node)
