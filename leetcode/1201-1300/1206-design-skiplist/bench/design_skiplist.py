# LeetCode #1206 bench, in Python: the ★ arm (a skiplist whose nodes live
# in a list, heights by coin flips from the list's own generator, erased
# slots reused) on 50000 calls drawn once, a third each of search, add and
# erase, on values up to 20000; then 10 rounds, each on a new list, every
# answer folded into a checksum.

LEVELS = 16


class Skiplist:
    def __init__(self):
        self.values = [0]
        self.next = [[-1] * LEVELS]
        self.free = []
        self.seed = 1206

    def height(self):
        h = 1
        while h < LEVELS:
            self.seed = (self.seed * 1103515245 + 12345) % 2147483648
            if (self.seed // 65536) % 2 == 1:
                break
            h += 1
        return h

    def path(self, target):
        path = [0] * LEVELS
        x = 0
        for level in range(LEVELS - 1, -1, -1):
            while self.next[x][level] >= 0 and self.values[self.next[x][level]] < target:
                x = self.next[x][level]
            path[level] = x
        return path

    def search(self, target):
        at = self.next[self.path(target)[0]][0]
        return at >= 0 and self.values[at] == target

    def add(self, num):
        path = self.path(num)
        h = self.height()
        links = [self.next[path[level]][level] for level in range(h)]
        if self.free:
            node = self.free.pop()
            self.values[node] = num
            self.next[node] = links
        else:
            self.values.append(num)
            self.next.append(links)
            node = len(self.values) - 1
        for level in range(h):
            self.next[path[level]][level] = node

    def erase(self, num):
        path = self.path(num)
        at = self.next[path[0]][0]
        if at < 0 or self.values[at] != num:
            return False
        for level in range(len(self.next[at])):
            if self.next[path[level]][level] == at:
                self.next[path[level]][level] = self.next[at][level]
        self.free.append(at)
        return True


seed = 1206


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    calls = []
    for _ in range(50000):
        op = next_random() % 3
        hi = next_random()
        calls.append((op, (hi * 32768 + next_random()) % 20001))
    check = 0
    for _ in range(10):
        lst = Skiplist()
        for op, v in calls:
            if op == 0:
                answer = lst.search(v)
            elif op == 1:
                lst.add(v)
                answer = True
            else:
                answer = lst.erase(v)
            check = (check * 131 + op * 2 + (1 if answer else 0)) % 1000000007
    print(f"10 rounds of 50000 calls: checksum {check}")


main()
