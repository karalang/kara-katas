# LeetCode #1206: Design Skiplist -- the ★ arm in Python: a skiplist whose
# nodes live in a list, each node's forward links one per level it stands
# on (-1 for none), node 0 the head on every level; a new node's height by
# coin flips from the list's own generator, up to 16, and an erased node's
# slot kept for the next add.

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


# ---- test harness ---------------------------------------------------------

seed = 1206


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def b(x):
    return "true" if x else "false"


def run(count, top):
    lst = Skiplist()
    found = erased = check = 0
    for _ in range(count):
        op = next_random() % 3
        hi = next_random()
        v = (hi * 32768 + next_random()) % top
        if op == 0:
            answer = lst.search(v)
            found += answer
        elif op == 1:
            lst.add(v)
            answer = True
        else:
            answer = lst.erase(v)
            erased += answer
        check = (check * 131 + op * 2 + (1 if answer else 0)) % 1000000007
    return f"{found} found, {erased} erased, checksum {check}"


def main():
    lst = Skiplist()
    lst.add(1)
    lst.add(2)
    lst.add(3)
    print(f"search(0): {b(lst.search(0))}")
    lst.add(4)
    print(f"search(1): {b(lst.search(1))}")
    print(f"erase(0): {b(lst.erase(0))}")
    print(f"erase(1): {b(lst.erase(1))}")
    print(f"search(1): {b(lst.search(1))}")
    dup = Skiplist()
    for _ in range(3):
        dup.add(5)
    dup.add(0)
    dup.add(20000)
    gone = [b(dup.erase(5)) for _ in range(4)]
    print(f"three 5s erased four times: [{', '.join(gone)}], search(5): {b(dup.search(5))}, search(0): {b(dup.search(0))}, search(20000): {b(dup.search(20000))}")
    empty = Skiplist()
    before = empty.search(7)
    empty.add(7)
    erased = empty.erase(7)
    print(f"empty: search(7) {b(before)}, add and erase(7) {b(erased)}, search(7) {b(empty.search(7))}, erase(7) {b(empty.erase(7))}")
    stairs = Skiplist()
    for v in range(1000):
        stairs.add(v)
    for v in range(999, -1, -1):
        if v % 2 == 0:
            stairs.erase(v)
    left = sum(1 for v in range(1000) if stairs.search(v))
    print(f"0..1000 added, the even ones erased: {left} left, search(999) {b(stairs.search(999))}, search(998) {b(stairs.search(998))}")
    lines = [run(100, 10) for _ in range(100)]
    check = 0
    for line in lines:
        for ch in line.encode():
            check = (check * 131 + ch) % 1000000007
    print(f"100 runs of 100 calls on values below 10: checksum {check}")
    print(f"50000 calls on values below 20001: {run(50000, 20001)}")
    print(f"50000 calls on values below 100: {run(50000, 100)}")


main()
