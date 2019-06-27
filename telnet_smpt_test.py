import itertools


class Graph:

    def __init__(self, possible_nodes):
        self.all_possible_nodes = possible_nodes
        self.nodes = list(itertools.permutations(possible_nodes, 2))
        self.answ = []

    def get_next_node(self, f, s):
        for next_f, next_s in [(i, j) for i, j in self.nodes if
                               i == s and j != f]:
            if not self.tmp_answ:
                self.tmp_answ.append((next_f, next_s))
                self.get_next_node(next_f, next_s)
            elif (next_f, next_s) not in self.tmp_answ:
                if len(self.tmp_answ) < len(self.all_possible_nodes) - 1 \
                        and not [(i, _) for i, _ in self.tmp_answ if
                                 i == next_s]:
                    self.tmp_answ.append((next_f, next_s))
                    self.get_next_node(next_f, next_s)

    def print_all_paths(self):
        for f, s in self.nodes:
            self.tmp_answ = []
            self.get_next_node(f, s)
            print(self.tmp_answ)
            self.answ.append(self.tmp_answ)




def generate_paths(nodes):
    all_variants = list(itertools.permutations(nodes, 2))
    total_answ = []
    for head in  all_variants:
        answ = []
        answ.append(head)
        for _ in range(len(nodes)):
            next_elem = [(e1, e2) for (e1, e2) in  all_variants
                         if e1 == head[1]
                         and e2 != head[0]
                         and all([True if i != e2 else False for i, j in answ])
                         ]
            if next_elem:
                next_elem = next_elem[0]
                if next_elem not in answ and next_elem not in map(lambda x: (x[1], x[0]), answ):
                    answ.append(next_elem)
                    head = next_elem
            else:
                break
        total_answ.append(answ)

print(generate_paths("ABCDE"))