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
    init_state = npuzzle.make_puzzle()
    print("Init   :", init_state.index)
    print("Answer :", init_state.answer)
    time, route = bfs(init_state)
    print("Time:", time)
    print("Length:", len(route))
    print("Route:", route)
