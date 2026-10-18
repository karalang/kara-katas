# LeetCode 752 — Open the Lock, breadth-first over numbers.
# Mirror of open_lock.kara (the ★ arm); same output, byte for byte.
from collections import deque


def open_lock(deadends, target):
    blocked = [False] * 10000
    for d in deadends:
        blocked[int(d)] = True
    goal = int(target)
    if blocked[0]:
        return -1
    dist = [-1] * 10000
    dist[0] = 0
    queue = deque([0])
    while queue:
        at = queue.popleft()
        if at == goal:
            return dist[at]
        place = 1
        for _ in range(4):
            digit = at // place % 10
            for step in (1, 9):
                nxt = at + ((digit + step) % 10 - digit) * place
                if not blocked[nxt] and dist[nxt] == -1:
                    dist[nxt] = dist[at] + 1
                    queue.append(nxt)
            place *= 10
    return -1


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(dead, target):
    deadends = dead.split(' ') if dead else []
    print(f"[{dead}], {target} -> {open_lock(deadends, target)}")


def four(x):
    return f"{x // 1000}{x // 100 % 10}{x // 10 % 10}{x % 10}"


def main():
    show("0201 0101 0102 1212 2002", "0202")
    show("8888", "0009")
    show("8887 8889 8878 8898 8788 8988 7888 9888", "8888")
    show("0000", "8888")
    show("", "0000")
    show("", "5555")
    show("1000 9000 0100 0900 0010 0090 0001", "1234")
    show("1000 9000 0100 0900 0010 0090 0001 0009", "1234")
    rng = Rng(752)
    total = 0
    stuck = 0
    check = 0
    for rnd in range(40):
        count = 1 + rng.next() % (12 * rnd + 10)
        deadends = [four(rng.next() % 10000) for _ in range(count)]
        target = four(rng.next() % 10000)
        turns = open_lock(deadends, target)
        if turns == -1:
            stuck += 1
        else:
            total += turns
        check = (check * 31 + turns + 1) % 1000000007
    print(f"40 random locks: {stuck} cannot open, the rest take {total} turns in all, checksum {check}")


main()
