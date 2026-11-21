# LeetCode #2349: Design a Number Container System -- the Python mirror of
# the ★ arm, lazy heaps: a dict from each index to its number, and for
# each number a heap of every index ever given it. A change only pushes;
# find pops the indices at the top that now hold another number.

import heapq


class NumberContainers:
    def __init__(self):
        self.at = {}
        self.heaps = {}

    def change(self, index, number):
        self.at[index] = number
        heapq.heappush(self.heaps.setdefault(number, []), index)

    def find(self, number):
        heap = self.heaps.get(number)
        if heap is None:
            return -1
        while heap:
            if self.at[heap[0]] == number:
                return heap[0]
            heapq.heappop(heap)
        return -1


def run(calls):
    containers = NumberContainers()
    answers = []
    for kind, a, b in calls:
        if kind == 0:
            containers.change(a, b)
        else:
            answers.append(containers.find(a))
    return answers


SEED = [2349]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def tally(answers, check):
    for a in answers:
        check = (check * 31 + a + 2) % 1000000007
    return check


def main():
    # LeetCode's example; an index changed twice; the largest index and
    # number; then 2 * 10^4 calls over 500 indices and 50 numbers
    print(" ".join(str(a) for a in run([(1, 10, 0), (0, 2, 10), (0, 1, 10), (0, 3, 10), (0, 5, 10), (1, 10, 0), (0, 1, 20), (1, 10, 0)])))
    print(" ".join(str(a) for a in run([(0, 1, 5), (0, 1, 6), (1, 5, 0), (1, 6, 0)])))
    print(" ".join(str(a) for a in run([(0, 1000000000, 1000000000), (1, 1000000000, 0), (0, 1, 1000000000), (1, 1000000000, 0)])))
    calls = []
    for i in range(20000):
        if i % 3 == 2:
            calls.append((1, i % 51 + 1, 0))
        else:
            calls.append((0, i * 7919 % 500 + 1, i % 50 + 1))
    answers = run(calls)
    found = sum(1 for a in answers if a >= 0)
    print(f"2 * 10^4 calls: checksum {tally(answers, 0)}, found {found} of {len(answers)}")
    # 2000 random scripts of 1 to 40 calls over indices 1 to 8 and numbers
    # 1 to 4, three changes to every two finds
    check = 0
    total = 0
    missing = 0
    for _ in range(2000):
        n = 1 + next_random() % 40
        calls = []
        for _ in range(n):
            if next_random() % 5 < 3:
                index = 1 + next_random() % 8
                calls.append((0, index, 1 + next_random() % 4))
            else:
                calls.append((1, 1 + next_random() % 4, 0))
        answers = run(calls)
        check = tally(answers, check)
        total += sum(answers)
        missing += sum(1 for a in answers if a < 0)
    print(f"2000 scripts: checksum {check}, sum {total}, missing {missing}")


main()
