import argparse
import sys

from npuzzle import *
from astar import astar
from bfs import bfs
from dfs import dfs
from ids import ids

fun_dic = {"astar" : astar, "bfs" : bfs, "dfs" : dfs, "ids" : ids}

def handle_args():
    state, fun = None, None

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--shake', type=int)

    group1 = parser.add_mutually_exclusive_group(required=True)
    group1.add_argument('-m', '--make', nargs=2)
    group1.add_argument('-i', '--input', type=str)
    group1.add_argument('-r', '--random', nargs='?', type=int, const=4)
    
    group2 = parser.add_mutually_exclusive_group(required=True)
    group2.add_argument('-a', '--algorithm', type=str)
    group2.add_argument('-c', '--compare', action='store_true')
   
    args = parser.parse_args()
    
    if args.make and (args.algorithm or args.compare):
        parser.error("-m option cannot be used with -a or -c option")

    if args.input and args.shake:
        parser.error("-s option cannot be used with -i option")

    if args.make:
        try:
            N = int(args.make[1])
            if str(N) != args.make[1] or (N < 2):
                raise ValueError
        except ValueError:
            print("ERROR : N must be positive integer greater than 1")
            sys.exit(-1)

        if args.shake:
            state = make_puzzle(N)
        else:
            state = make_puzzle_shake(N, args.shake)

        with open(args.make[0], 'wt') as f:
            for x in state.index:
                f.write(str(x) + ' ')
            f.write('\n')
        return args, state, fun

    if args.input:
        with open(args.input, 'rt') as f:
            idx_str = f.readline()
            init_idx = idx_str.split()
            N = int(len(init_idx)**0.5)
            state = State(N, tuple(init_idx))
    else:
        if args.shake:
            state = make_puzzle_shake(args.random, args.shake)
        else:
            state = make_puzzle(args.random)

    if args.compare:
        return args, state, fun
    else:
        alg_name = args.algorithm
        if alg_name in fun_dic.keys():
            fun = fun_dic[alg_name]
        else:
            parser.error("-a option must be 'astar', 'bfs', 'dfs', or 'ids'. Yours = '{}'".format(alg_name))
        return args, state, fun

def run(init_state, fun):
    print("Init :")
    State.print_state(init_state.index)
    print()

    time, route = fun(init_state)
    print("Changed :")
    State.print_state(init_state.answer)
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

def compare(init_state):
    print("Init       :")
    State.print_state(init_state.index)
    print()

    time_list = []
    length_list = []

    for fun in fun_dic.values():
        time, route = fun(init_state)
        time_list.append(str(time))
        length_list.append(str(len(route)))

    fun_list = ["{:^5}".format(x) for x in fun_dic.keys()]
    time_list = ["{:^5}".format(x) for x in time_list]
    length_list = ["{:^5}".format(x) for x in length_list]

    print("Comparison :")
    print()
    print("       | " + '  '.join(fun_list))
    print("-"*35)
    print("Time   | " + '  '.join(time_list))
    print("Length | " + '  '.join(length_list))


def main():
    args, init_state, fun = handle_args()

    if args.make:
        return
    elif args.compare:
        compare(init_state)
    else:
        run(init_state, fun)
   
if __name__ == "__main__":
    main()
