import random

class State():
    def __init__(self, N, index, prev=None, way=None, depth=0):
        self.N = N
        self.puzzle_size = N**2
        self.answer = tuple([str(x) for x in range(1, N**2)]+['X'])
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
        pos = self.index.index('X')
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
        while tmp_node.prev:
            result.append(tmp_node.way)
            tmp_node = tmp_node.prev
        result.reverse()
        return result

    @staticmethod
    def print_state(index):
        N = int(len(index)**0.5)
        for i in range(N):
            print(' --'*N + ' ')
            line = '|'.join(["{:^2}".format(x) for x in index[i*N:(i+1)*N]])
            line = '|' + line
            line += '|'   
            print(line)
        print(' --'*N + ' ')


def manhattan_dist(i1, i2, N):
    a, b = i1//N, i1%N
    c, d = i2//N, i2%N
    return abs(a-c) + abs(b-d)

def total_manhattan_dist(s1, s2):
    result = 0
    
    for s1_idx in range(s1.puzzle_size):
        s1_val = s1.index[s1_idx]
        if s1_val != 'X':
            s2_idx = s2.index.index(s1_val)
            result += manhattan_dist(s1_idx, s2_idx, s1.N)
    return result


def make_pair(x):
    result = []
    for i in range(len(x)-1):
        for j in range(i+1, len(x)):
            result.append((x[i], x[j]))
    return result

def linear_conflict_line(line1, line2):
    result = 0
    for x, y in zip(line1, line2):
        overlap = set(x).intersection(set(y))
        overlap = overlap.difference(set(['X']))
        pairs = make_pair(list(overlap))
        for m, n in pairs:
            diff1 = x.index(m) - x.index(n)
            diff2 = y.index(m) - y.index(n)
            if diff1*diff2 < 0:
                result += 1
    return result

def linear_conflict(s1, s2):
    N = int(len(s1)**0.5)
    rows1 = [tuple(s1[i*N:(i+1)*N]) for i in range(N)]
    rows2 = [tuple(s2[i*N:(i+1)*N]) for i in range(N)]

    cols1 = tuple(zip(*rows1))
    cols2 = tuple(zip(*rows2))

    row_conflict = linear_conflict_line(rows1, rows2)
    col_conflict = linear_conflict_line(cols1, cols2)

    return row_conflict + col_conflict


def number_of_cycles(s1, s2):
    s1 = s1
    s2 = s2

    cnt = 0
    cnt_list = list(range(len(s1))) # remaining index of s1
    new_cycle_flag = True
    total_cycle = []

    while cnt_list:
        if new_cycle_flag:
            cycle = set()
            total_cycle.append(cycle)

        cnt_list.pop(cnt_list.index(cnt))
        cycle.add(s1[cnt])

        if s2[cnt] in cycle:
            if cnt_list:
                cnt = cnt_list[0]
            new_cycle_flag = True
        else:    
            if new_cycle_flag:
                new_cycle_flag = False
            cnt = s1.index(s2[cnt])

    return len(total_cycle)

def total_parity(s1, s2):
    N = int(len(s1)**0.5)
    s1_idx = s1.index('X')
    s2_idx = s2.index('X')
    
    return (number_of_cycles(s1, s2)
          + manhattan_dist(s1_idx, s2_idx, N))%2

def make_puzzle(N):
    answer_idx = [str(x) for x in range(1, N**2)]+['X']
    init_idx = answer_idx[:]
    random.shuffle(init_idx)

    if total_parity(init_idx, answer_idx) != (N**2)%2:
        if init_idx.index('X') in [0, 1]:
            init_idx[2], init_idx[3] = init_idx[3], init_idx[2]
        else:
            init_idx[0], init_idx[1] = init_idx[1], init_idx[0]
    init_state = State(N, tuple(init_idx))
    return init_state

def make_puzzle_shake(N, k):
    init_idx =[str(x) for x in range(1, N**2)]+['X']
    for i in range(k):
        pos = init_idx.index('X')
        new_pos = random.choice([p for p, _ in State.next_pos(N, pos)])
        init_idx[pos], init_idx[new_pos] = init_idx[new_pos], init_idx[pos]
    init_state = State(N, tuple(init_idx))
    return init_state

if __name__ == "__main__":
    s = make_puzzle(4)
    State.print_state(s.index)
