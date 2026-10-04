# Benchmark mirror of nested_weight_sum.kara (LeetCode #339): parse a list's
# text into the tree, then walk it. Same lists, rounds and sink.
import sys

sys.setrecursionlimit(100000)


def depth_sum(items, depth):
    total = 0
    for item in items:
        if isinstance(item, list):
            total += depth_sum(item, depth + 1)
        else:
            total += item * depth
    return total


def weight_sum(items):
    return depth_sum(items, 1)


def parse_list(text, pos):
    items = []
    pos += 1
    while text[pos] != "]":
        if text[pos] == ",":
            pos += 1
        elif text[pos] == "[":
            inner, pos = parse_list(text, pos)
            items.append(inner)
        else:
            sign = 1
            if text[pos] == "-":
                sign = -1
                pos += 1
            v = 0
            while text[pos].isdigit():
                v = v * 10 + (ord(text[pos]) - ord("0"))
                pos += 1
            items.append(sign * v)
    return items, pos + 1


def parse(text):
    return parse_list(text, 0)[0]


class Rng:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (self.state * 1103515245 + 12345) % 2147483648
        return self.state >> 8


def gen_member(rng, depth, max_depth, out):
    if depth < max_depth and rng.next() % 3 == 0:
        out.append("[")
        count = rng.next() % 5
        for k in range(count):
            if k > 0:
                out.append(",")
            gen_member(rng, depth + 1, max_depth, out)
        out.append("]")
    else:
        out.append(str(rng.next() % 201 - 100))


def gen_text(seed, top, max_depth):
    rng = Rng(seed)
    out = ["["]
    for k in range(top):
        if k > 0:
            out.append(",")
        gen_member(rng, 1, max_depth, out)
    out.append("]")
    return "".join(out)



texts = [gen_text(s * 7919 + 1, 800, 12) for s in range(8)]
h = 0
for r in range(4000):
    w = weight_sum(parse(texts[r % 8]))
    h = (h * 31 + w + 1000000) % 1000000007
print(h)
