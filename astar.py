import heapq
import sys

import npuzzle

def gbfs(init_state):
    return astar_body(init_state, lambda node : 0)

def astar(init_state):
    return astar_body(init_state, lambda node : node.depth)

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

if __name__ == '__main__':
    #init_state = npuzzle.make_puzzle_shake(3, 100)
    init_state = npuzzle.make_puzzle(4)
    print("Init    :")
    npuzzle.State.print_state(init_state.index)
    print()

    time, route = astar(init_state)
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
