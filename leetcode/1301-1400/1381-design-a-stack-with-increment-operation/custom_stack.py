# LeetCode #1381: Design a Stack With Increment Operation -- Python
# mirror of the ★ arm: an increment is owed to the element k places up
# and left there; a pop pays the top element what it is owed and hands
# the debt down to the one below.

seed = 1381


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


class CustomStack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.stack = []
        self.owed = []

    def push(self, x):
        if len(self.stack) < self.max_size:
            self.stack.append(x)
            self.owed.append(0)

    def pop(self):
        if not self.stack:
            return -1
        x = self.stack.pop()
        debt = self.owed.pop()
        if self.owed:
            self.owed[-1] += debt
        return x + debt

    def increment(self, k, val):
        reach = min(len(self.stack), k)
        if reach > 0:
            self.owed[reach - 1] += val


def main():
    s = CustomStack(3)
    answers = []
    s.push(1)
    s.push(2)
    answers.append(s.pop())
    s.push(2)
    s.push(3)
    s.push(4)
    s.increment(5, 100)
    s.increment(2, 100)
    for _ in range(4):
        answers.append(s.pop())
    print(" ".join(map(str, answers)))
    answers = []
    s = CustomStack(1)
    s.push(5)
    s.push(6)
    s.increment(1000, 100)
    answers.append(s.pop())
    answers.append(s.pop())
    s.increment(3, 7)
    s.push(4)
    answers.append(s.pop())
    s = CustomStack(3)
    s.push(1)
    s.push(2)
    s.push(3)
    s.increment(2, 10)
    answers.append(s.pop())
    s.push(7)
    s.increment(3, 5)
    for _ in range(4):
        answers.append(s.pop())
    print(" ".join(map(str, answers)))
    s = CustomStack(1000)
    for _ in range(1000):
        s.push(1 + next_random() % 1000)
    for _ in range(1000):
        k = 1 + next_random() % 1000
        val = next_random() % 101
        s.increment(k, val)
    check = 0
    for _ in range(1000):
        check = (check * 131 + s.pop()) % 1000000007
    print(f"3000 calls: checksum {check}")
    check = 0
    pops = 0
    empty = 0
    for c in range(2000):
        s = CustomStack(1 + next_random() % 20)
        calls = 1 + next_random() % 100
        push, pop = [(4, 7), (6, 8), (3, 6), (5, 9)][c % 4]
        for _ in range(calls):
            r = next_random() % 10
            if r < push:
                s.push(1 + next_random() % 1000)
            elif r < pop:
                got = s.pop()
                pops += 1
                if got == -1:
                    empty += 1
                check = (check * 131 + got + 1) % 1000000007
            else:
                k = 1 + next_random() % 25
                val = next_random() % 101
                s.increment(k, val)
    print(f"2000 random sessions: {pops} pops, {empty} of an empty stack, checksum {check}")


main()
