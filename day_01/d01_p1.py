from collections import Counter

class ListComparator:
    def __init__(self, input_path):
        self.list1, self.list2 = self.read_file(input_path)
        self.list1.sort()
        self.list2.sort()

    def read_file(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            list1 = [int(line.split()[0]) for line in lines]
            list2 = [int(line.split()[1]) for line in lines]
        return list1, list2

    def compare(self):
        return sum(abs(a - b) for a, b in zip(self.list1, self.list2))

    def similarity_score(self):
        l2_cts = Counter(self.list2)
        sim_score = sum([x * l2_cts.get(x, 0) for x in self.list1])
        return sim_score

if __name__ == '__main__':

    lc = ListComparator('input_d01p1.txt')
    print(lc.compare())
    print(lc.similarity_score())
