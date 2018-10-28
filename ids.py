import sys
import math
import npuzzle

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

def ids(init_state):
    """Iteration version iterative-deepening search."""
    time = 0
    for depth in range(math.factorial(init_state.puzzle_size)//2):
        depth_time, result = dls(init_state, depth)
        time += depth_time
        if result != ('C' or 'F'):
            return time, result

    if result == 'C':
        print("FAILED: cutoff")
    elif result == 'F':
        print("FAILED: failed")

if __name__ == '__main__':
    init_state = npuzzle.make_puzzle()
    print("Init   :", init_state.index)
    print("Answer :", init_state.answer)

    time, route = ids(init_state)
    print("Time:", time)
    print("Length:", len(route))
    print("Route:", route)
