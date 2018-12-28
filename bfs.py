import sys

from collections import deque
import npuzzle

def bfs(init_state):
    if init_state.goal_test():
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
                    return len(explored), new_state.backtrace()
                else:
                    d.appendleft(new_state)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)

if __name__ == '__main__':
    init_state = npuzzle.make_puzzle(2)
    print("Init    :")
    npuzzle.State.print_state(init_state.index)
    print()

    time, route = bfs(init_state)
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
