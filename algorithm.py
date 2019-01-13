import sys
import math
import heapq
from collections import deque

import npuzzle

def gbfs(init_state, return_dict):
    time, route = astar_body(init_state, lambda node : 0)
    return_dict["gbfs"] = (time, route)
    return time, route

def astar(init_state, return_dict):
    time, route = astar_body(init_state, lambda node : node.depth)
    return_dict["astar"] = (time, route)
    return time, route

def astar_body(init_state, g):
    """A* algorithm. Return explored indices and goal index."""
    def f(node):
        """Returns g+h value.

        g : cost from start to now(depth)
        h : heuristic function(MD+ED/MD-1)
        """           
        answer_state = npuzzle.State(node.N, node.answer)
        h = npuzzle.total_manhattan_dist(node, answer_state) +\
            2*npuzzle.linear_conflict(node.index,node.answer)
        return g(node) + h
    
    explored = set()
    # Push tuple (f, idx) to the heap
    h = [(f(init_state), init_state)]
    while h:
        elm = heapq.heappop(h)
        node = elm[1]
        explored.add(node.index)
        
        # Goal test
        if node.goal_test():
            return len(explored), node.backtrace()

        for new_state in node.next_state():
            i = find_value(h, new_state)
            if new_state.index not in explored and i == None:
                heapq.heappush(h, (f(new_state), new_state))
            elif i != None and f(new_state) < h[i][0]:
                h.pop(i)
                heapq.heappush(h, (f(new_state), new_state))
                
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

def find_value(h, state):
    for i in range(len(h)):
        if h[i][1] == state:
            return i
    return None


def bfs(init_state, return_dict):
    if init_state.goal_test():
        return_dict["bfs"] = (0, [])
        return 0, []

    explored = set()
    d = deque()

    d.append(init_state)
    while d:   
        node = d.pop()
        explored.add(node.index)
        for new_state in node.next_state():
            if new_state.index not in explored and new_state not in d:
                # Goal test
                if new_state.goal_test():
                    time = len(explored)
                    route = new_state.backtrace()
                    return_dict["bfs"] = (time, route)
                    return time, route
                else:
                    d.appendleft(new_state)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)


def dfs(init_state, return_dict):
    explored = set()
    s = [init_state]

    while s:   
        node = s.pop()
        explored.add(node.index)

        # Goal test
        if node.goal_test():
            time = len(explored)
            route = node.backtrace()
            return_dict["dfs"] = (time, route)
            return time, route

        for new_state in node.next_state():
            if new_state.index not in explored and new_state not in s:
                s.append(new_state)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)


def dls(init_state, depth):
    """Iteration version Depth-limeted search."""
    explored = set()
    s = [init_state]

    # Goal test
    if init_state.goal_test():
        return len(explored), init_state.backtrace()

    while s:   
        node = s.pop()
        explored.add(node.index)

        for new_state in node.next_state():
            if new_state.index not in explored and new_state not in s and new_state.depth <= depth:
                # Goal test
                if new_state.goal_test():
                    return len(explored), new_state.backtrace()
                else:
                    s.append(new_state)
    else:
        return len(explored), 'C'

def ids(init_state, return_dict):
    """Iteration version iterative-deepening search."""
    time = 0
    for depth in range(math.factorial(init_state.puzzle_size)//2):
        depth_time, route = dls(init_state, depth)
        time += depth_time
        if route != ('C' or 'F'):
            return_dict["ids"] = (time, route)
            return time, route

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")

if __name__ == '__main__':
    #init_state = npuzzle.make_puzzle_shake(3, 100)
    init_state = npuzzle.make_puzzle(4)
    print("Init    :")
    npuzzle.State.print_state(init_state.index)
    print()

    time, route = astar(init_state, {})
    print("Changed :")
    npuzzle.State.print_state(init_state.answer)
    print()

    print("Time    :", time)
    print("Length  :", len(route))
    print("Route   :")
    print()

    print("   |  0  1  2  3  4  5  6  7  8  9 ")
    print("-----------------------------------")
    for i, r in enumerate(route):
        if i%10 == 0:
            print('{:2} | '.format(i), end=' ')
        print(r, end='  ')

        if i%10 == 9:
            print()
    print()
