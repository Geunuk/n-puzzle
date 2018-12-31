# n-puzzle

This program find time and length to get answer state of n-puzzle using several algorithms.
Time means number of explored states before answer state.
Length means number of moves from initial state to answer state

## Supported Algorithms
* A*(astar) - heuristic: linear conflict
* Greedy Best First Search(gbfs)
* Breadth First Search(bfs)
* Depth First Search(dfs)
* Iterative Deepening Search(ids)

## Notice
Because number of cases of n-puzzle is to big, bfs, dfs and ids can take quite a long time.
A* work well at 8-puzzle. And also work well at 15-puzzle with -s option when small [count] used.

## Make Input File

```
$python3 main.py -m [file name]
```
Also, you can make not totally random input file.
-s option make input state using [count] random moves from answer state.

```
$python3 main.py -m [file name] -s [count]
```


## Run Algorithm
Insert input file and set algorithm between astar, gbfs, bfs, dfs or ids
```
$python3 main.py -i [file name] -a [alg]
```
You can also use random state puzzle. It's possible to set difficulty using -s option.
```
$python3 main.py -r [size] -a [alg]
```

```
$python3 main.py -r [size] -s [count] -a [alg]
```
## Compare Algorithms
Similar with 'Run', but add -c option.

```
$python3 main.py -c -i [file name]
```

```
$python3 main.py -c -r [size]
```

```
$python3 main.py -c -r [size] -s [count]
```

## Solvability of n-puzzle
For solvability of n-puzzle, please look https://geunuk.wordpress.com/2018/12/25/n-puzzle/
