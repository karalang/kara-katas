# LeetCode #341: Flatten Nested List Iterator.
# Mirrors flatten_iterator.kara (the ★ arm) and prints the same lines.
# A nested member is a Python int or a Python list of members.


class NestedIterator:
    def __init__(self, items):
        self.stack = []
        self.push_reversed(items)

    def push_reversed(self, items):
        rest = list(items)
        while rest:
            self.stack.append(rest.pop())

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


def flatten(items):
    it = NestedIterator(items)
    out = []
    while it.has_next():
        out.append(it.next())
    return out


# ---- input ----------------------------------------------------------------


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


def render(vals):
    return "[" + ",".join(str(v) for v in vals) + "]"


def digest(vals):
    h = 7
    for v in vals:
        h = (h * 31 + v + 101) % 1000000007
    return f"{len(vals)} integers, sum {sum(vals)}, hash {h}"


def show(text):
    print(f"{text} -> {render(flatten(parse(text)))}")


def summary(seed, top, max_depth):
    text = gen_text(seed, top, max_depth)
    vals = flatten(parse(text))
    print(
        f"seed {seed}, {top} members, depth up to {max_depth}: "
        f"{len(text)} chars, {digest(vals)}"
    )


def main():
    show("[[1,1],2,[1,1]]")
    show("[1,[4,[6]]]")
    show("[]")
    show("[[]]")
    show("[[],[[]],7]")
    show("[-3,[-4,[5,[-6]]]]")
    show("[[[[[[[[[[9]]]]]]]]]]")
    show("[0,[0,[0]],1000000]")
    summary(1, 10, 4)
    summary(7, 1000, 8)
    summary(42, 20000, 12)
    summary(2026, 50000, 30)


main()
