import pickle
import npuzzle
from astar import astar
from bfs import bfs
from ids import ids
from dfs import dfs

def make_input(file_name, N):
    init_state = npuzzle.make_puzzle_parity(N)
    with open(file_name, 'wb') as f:
        pickle.dump(init_state, f)

def calculate_and_print(f, init_state):
    time, route = f(init_state)
    print("-"*60)
    print("[{}]".format(f.__name__))
    print("Time:", time)
    print("Length:", len(route))
    print("Route:", route)

def compare_algorithm(N):
    #with open(file_name, 'rb') as f:
    #    init_state = pickle.load(f)
   
    init_state = npuzzle.make_puzzle(N)
    print("N      :", init_state.N)
    print("Init   :", init_state.index)
    print("Answer :", init_state.answer)


    fun_list = [astar, bfs, ids, dfs]
    result = {}
    for fun in algorithm_list:
        time, route = fun(init_state)
        result[fun] = (time, route)

        #calculate_and_print(algorithm, init_state)

if __name__ == "__main__":
    #file_name = "input_1.dat" 
    #make_input(file_name, 2)
    compare_algorithm(2)
