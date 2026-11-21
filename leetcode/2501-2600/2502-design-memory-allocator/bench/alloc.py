# LeetCode #2502: Design Memory Allocator -- benchmark mirror of the ★
# arm (alloc.kara): sessions of 1000 calls on 1000 units, each call drawn
# from the generator and from the checksum so far.


class Allocator:
    def __init__(self, n):
        self.memory = [0] * n

    def allocate(self, size, m_id):
        run = 0
        for i in range(len(self.memory)):
            if self.memory[i] == 0:
                run += 1
                if run == size:
                    start = i + 1 - size
                    for j in range(start, i + 1):
                        self.memory[j] = m_id
                    return start
            else:
                run = 0
        return -1

    def free_memory(self, m_id):
        freed = 0
        for i in range(len(self.memory)):
            if self.memory[i] == m_id:
                self.memory[i] = 0
                freed += 1
        return freed


seed = 2502


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    sessions = 400
    check = 0
    for s in range(sessions):
        allocator = Allocator(1000)
        for _ in range(1000):
            if (next_random() + check) % 3 < 2:
                r = allocator.allocate(next_random() % 20 + 1, next_random() % 50 + 1)
            else:
                r = allocator.free_memory(next_random() % 50 + 1)
            check = (check * 31 + r + 1 + s) % 1000000007
    print(f"{sessions} sessions of 1000 calls on 1000 units: checksum {check}")


main()
