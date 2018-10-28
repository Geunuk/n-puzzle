from collections import deque
import math
import pickle
import npuzzle

def class_size(init_state):
    explored = set()
    d = deque()
    d.append(init_state)

    n = 0
    while d:   
        node = d.pop()
        #answer_state = npuzzle.State(N, node.answer)
        #print("parity:", npuzzle.total_parity(node, answer_state)) 
        explored.add(node.index)
        
        n += 1
        if n == 10000:
            print(n)

        for new_state in node.next_state():
            if new_state.index not in explored and new_state not in d:
                d.appendleft(new_state)

    return explored

def include_test(file_name, tup):
    with open(file_name, "rb") as infile:
        size = pickle.load(infile)
    return tup in size

if __name__ == '__main__':
    N = int(input("How big is your puzzle? : "))

    init_idx = tuple(range(N**2))
    init_state = npuzzle.State(N,init_idx)

    size = class_size(init_state)

    file_name = "size_" + str(N) + ".dat"
    with open(file_name, "wb") as outfile:
        pickle.dump(size, outfile)

    print("Class 1 Size:", len(size))
 
    init_idx = list(range(N**2))
    init_idx[1], init_idx[1+N] = init_idx[1+N], init_idx[1]
    init_state = npuzzle.State(N,tuple(init_idx))

    size = class_size(init_state)
    print("Class 2 Size:", len(size))
        
    #print(include_test(file_name, (0,3,1,2)))
