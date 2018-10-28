import sys
import npuzzle

def dfs(init_state):
    explored = set()
    s = [init_state]

    while s:   
        node = s.pop()
        explored.add(node.index)

        # Goal test
        if node.goal_test():
            return len(explored), node.backtrace()

        for new_state in node.next_state():
            if new_state.index not in explored and new_state not in s:
                s.append(new_state)
    else:
        print("FAILED: cannot found figure")
        sys.exit(-1)
        
if __name__ == '__main__':
    init_state = npuzzle.make_puzzle()
    print("Init   :", init_state.index)
    print("Answer :", init_state.answer)

    time, route = dfs(init_state)
    print("Time:", time)
    print("Length:", len(route))
    print("Route:", route)
