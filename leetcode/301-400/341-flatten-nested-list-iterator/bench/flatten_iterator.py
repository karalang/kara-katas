# Benchmark kernel for LeetCode #341 (Flatten Nested List Iterator).
# Mirrors flatten_iterator.kara: a stack of members, with has_next()
# expanding lists until an integer is on top. A member is a Python int or a
# Python list of members.


class NestedIterator:
    def __init__(self, items):
        self.stack = []
        self.push_reversed(items)

    def push_reversed(self, items):
        while items:
            self.stack.append(items.pop())

    def has_next(self):
        while self.stack:
            top = self.stack.pop()
            if isinstance(top, int):
                self.stack.append(top)
                return True
            self.push_reversed(top)
        return False

    def next(self):
        self.has_next()
        if self.stack and isinstance(self.stack[-1], int):
            return self.stack.pop()
        raise RuntimeError("next() past the end")


class Rng:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * 1103515245 + 12345) % 2147483648
        return self.state >> 8


def gen_member(rng, depth, max_depth):
    if depth < max_depth and rng.next() % 3 == 0:
        count = rng.next() % 5
        return [gen_member(rng, depth + 1, max_depth) for _ in range(count)]
    return rng.next() % 201 - 100


def gen_list(seed, top, max_depth):
    rng = Rng(seed)
    return [gen_member(rng, 1, max_depth) for _ in range(top)]


def main():
    h = 7
    for r in range(80):
        it = NestedIterator(gen_list(r * 7 + 1, 20000, 12))
        while it.has_next():
            h = (h * 31 + it.next() + 101) % 1000000007
    print(h)


main()
