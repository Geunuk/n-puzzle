import random

class State():
    def __init__(self, N, index, prev=None, way=None, depth=0):
        self.N = N
        self.puzzle_size = N**2
        self.answer = tuple(range(N**2))
        self.index = index
        self.prev = prev
        self.way = way
        self.depth = depth

    def __lt__(self, other):
        return other

    def __eq__(self, other):
        return self.index == other.index

    def goal_test(self):
        return self.index == self.answer

    def next_state(self):
        pos = self.index.index(0)
        result = []
        for new_pos, way in State.next_pos(self.N, pos):
            new_idx = list(self.index[:])
            new_idx[pos], new_idx[new_pos] = new_idx[new_pos], new_idx[pos]
            result.append(State(self.N, tuple(new_idx),self,way,self.depth+1))
        return result

    @staticmethod
    def next_pos(N, idx):
        q, r = idx//N, idx%N

        if q-1 >= 0:
            yield N*(q-1) + r, '^'
        if q+1 <= N-1:
            yield N*(q+1) + r, '_'
        if r-1 >= 0:
            yield N*q + r-1, '<'
        if r+1 <= N-1:
            yield N*q + r+1, '>'

    def backtrace(self):
        result = []
        tmp_node = self
        #while tmp_node.prev != None:
        while tmp_node.prev:
            result.append(tmp_node.way)
            tmp_node = tmp_node.prev
        result.reverse()
        return result

def manhattan_dist(i1, i2, N):
    a, b = i1//N, i1%N
    c, d = i2//N, i2%N
    return abs(a-c) + abs(b-d)

def total_manhattan_dist(s1, s2):
    result = 0

    for s1_idx in range(s1.puzzle_size):
        s1_val = s1.index[s1_idx]
        s2_idx = s2.index.index(s1_val)
        result += manhattan_dist(s1_idx, s2_idx, s1.N)
    return result

def parity_of_permutation(s1, s2):
    s1_idx = s1.index
    s2_idx = s2.index

    cnt = 0
    cnt_list = list(range(s1.puzzle_size)) # remaining index of s1
    new_cycle_flag = True
    total_cycle = []

    while cnt_list:
        if new_cycle_flag:
            cycle = set()
            total_cycle.append(cycle)

        cnt_list.pop(cnt_list.index(cnt))
        cycle.add(s1_idx[cnt])

        if s2_idx[cnt] in cycle:
            if cnt_list:
                cnt = cnt_list[0]
            new_cycle_flag = True
        else:    
            if new_cycle_flag:
                new_cycle_flag = False
            cnt = s1_idx.index(s2_idx[cnt])

    return len(total_cycle)%2

def parity_of_taxicab_dist(s1, s2):
    s1_idx = s1.index.index(0)
    s2_idx = s2.index.index(0)
    return manhattan_dist(s1_idx, s2_idx, s1.N)%2

def total_parity(s1, s2):
    return (parity_of_permutation(s1,s2) + parity_of_taxicab_dist(s1,s2))%2

def make_puzzle():
    """Get the number of shakes from keyboard.
    
    Move puzzle at state [0,1,...,PUZZLE_SIZE-1] and move puzzle n times

    Returns:
        init_state: moved state
    """

    N = int(input("How big is your puzzle? : "))
    k = int(input("How many times shake puzzle? : "))

    init_idx = list(range(N**2))
    for i in range(k):
        pos = init_idx.index(0)
        new_pos = random.choice([p for p, _ in State.next_pos(N, pos)])
        init_idx[pos], init_idx[new_pos] = init_idx[new_pos], init_idx[pos]

    init_state = State(N, tuple(init_idx))
    return init_state

def make_puzzle_parity(N):
    init_idx = list(range(N**2))
    answer_idx = init_idx[:]

    random.shuffle(init_idx)
    init_state = State(N, tuple(init_idx))
    answer_state = State(N, tuple(answer_idx))

    if total_parity(init_state, answer_state):
        if init_idx.index(0) in [0, 1]:
            init_idx[2], init_idx[3] = init_idx[3], init_idx[2]
        else:
            init_idx[0], init_idx[1] = init_idx[1], init_idx[0]

        init_state = State(N, tuple(init_idx))
    return init_state

if __name__ == "__main__":
    #print(parity_of_permutation(State(2, (0,3,2,1)),State(2, (0,3,2,1))))
    #print(total_manhattan_dist(State(2, (1,3,2,0)),State(2, (3,2,1,0))))
    N = 2
    print(total_parity(make_puzzle_parity(N), State(N, tuple(range(N**2)))))
