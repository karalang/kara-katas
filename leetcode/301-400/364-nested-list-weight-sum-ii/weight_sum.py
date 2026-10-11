# LeetCode #364: Nested List Weight Sum II -- mirror of weight_sum.kara.
# An integer is an int and a list is a Python list.


def max_depth(items, depth):
    deepest = 0
    for item in items:
        if isinstance(item, int):
            deepest = max(deepest, depth)
        else:
            deepest = max(deepest, max_depth(item, depth + 1))
    return deepest


def weighted(items, depth, top):
    total = 0
    for item in items:
        if isinstance(item, int):
            total += item * (top - depth + 1)
        else:
            total += weighted(item, depth + 1, top)
    return total


def depth_sum_inverse(items):
    return weighted(items, 1, max_depth(items, 1))


def parse_item(s, at):
    if s[at] == "[":
        at += 1
        items = []
        while s[at] != "]":
            item, at = parse_item(s, at)
            items.append(item)
            if s[at] == ",":
                at += 1
        return items, at + 1
    sign = 1
    if s[at] == "-":
        sign, at = -1, at + 1
    v = 0
    while s[at].isdigit():
        v = v * 10 + int(s[at])
        at += 1
    return sign * v, at


def parse(s):
    item, _ = parse_item(s, 0)
    return item if isinstance(item, list) else []


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_list(rng, depth, out):
    out.append("[")
    n = rng.next() % 5
    for i in range(n):
        if i > 0:
            out.append(",")
        if depth < 6 and rng.next() % 3 == 0:
            random_list(rng, depth + 1, out)
        else:
            out.append(str(rng.next() % 201 - 100))
    out.append("]")


def show(label, text):
    print(f"{label}: {depth_sum_inverse(parse(text))}")


def main():
    show("example 1", "[[1,1],2,[1,1]]")
    show("example 2", "[1,[4,[6]]]")
    show("an empty list", "[]")
    show("only empty lists", "[[],[[]]]")
    show("one integer", "[5]")
    show("empty lists below the deepest integer", "[1,[[]]]")
    show("a level with no integers", "[1,[[2]]]")
    show("the deep integer first", "[[[7]],1]")
    show("negative integers", "[-3,[2,[-1]]]")
    show("one integer five lists down", "[[[[[1]]]]]")
    show("a staircase", "[1,[2],[[3]],[[[4]]]]")
    rng = Rng(364)
    checksum = 0
    for _ in range(500):
        out = []
        random_list(rng, 1, out)
        checksum = (checksum * 31 + depth_sum_inverse(parse("".join(out))) + 1000000) % 1000000007
    print(f"500 random lists: checksum {checksum}")


main()
