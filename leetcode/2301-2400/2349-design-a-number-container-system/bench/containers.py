# LeetCode #2349: Design a Number Container System -- the bench, the ★ arm
# in Python: a dict from each index to its number, and for each number a
# heap of every index ever given it, popped lazily by find.

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


SEED = [2349]


def next_random():
    SEED[0] = (SEED[0] * 1103515245 + 12345) % 2147483648
    return SEED[0] // 65536


def main():
    # two changes to every find, over 10^5 indices and 1000 numbers
    calls = []
    for _ in range(200000):
        if next_random() % 3 < 2:
            high = next_random()
            index = (high * 32768 + next_random()) % 100000 + 1
            calls.append((0, index, next_random() % 1000 + 1))
        else:
            calls.append((1, next_random() % 1000 + 1, 0))
    check = 0
    for p in range(20):
        containers = NumberContainers()
        for kind, a, b in calls:
            if kind == 0:
                containers.change(a, b)
            else:
                check = (check * 31 + containers.find(a) + p + 2) % 1000000007
    print(f"20 passes over 2 * 10^5 calls: checksum {check}")


main()
