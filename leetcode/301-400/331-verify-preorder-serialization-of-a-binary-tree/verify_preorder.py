# LeetCode #331: Verify Preorder Serialization of a Binary Tree — slot counting.
# Python mirror of verify_preorder.kara; prints the same lines.
import sys

sys.setrecursionlimit(100000)


def is_valid_serialization(preorder):
    slots = 1
    for tok in preorder.split(","):
        if slots == 0:
            return False
        if tok == "#":
            slots -= 1
        else:
            slots += 1
    return slots == 0


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_tree(rng, budget, fill, out):
    if budget[0] > 0 and rng.next() % 100 < fill:
        budget[0] -= 1
        out.append(str(rng.next() % 100))
        random_tree(rng, budget, fill, out)
        random_tree(rng, budget, fill, out)
    else:
        out.append("#")


def b(v):
    return "true" if v else "false"


def show(s):
    print(f'"{s}" -> {b(is_valid_serialization(s))}')


def main():
    show("9,3,4,#,#,1,#,#,2,#,6,#,#")
    show("1,#")
    show("9,#,#,1")
    show("#")
    show("#,#")
    show("1")
    show("1,#,#")
    show("1,#,#,#")
    show("#,1,#,#")
    show("100,99,#,#,0,#,#")
    show("1,2,3,#,#,#,#")
    show("1,2,3,#,#,#")
    rng = Rng(331)
    for rnd in range(6):
        budget = [3 + rnd * 4]
        parts = []
        random_tree(rng, budget, 75, parts)
        whole = ",".join(parts)
        cut = parts[:-1]
        cut_s = ",".join(cut)
        print(f"random {rnd}: {len(parts)} tokens -> {b(is_valid_serialization(whole))}, "
              f"last dropped -> {b(is_valid_serialization(cut_s))}")
    budget = [5000]
    parts = []
    random_tree(rng, budget, 95, parts)
    big = ",".join(parts)
    extra = big + ",#"
    print(f"big: {len(parts)} tokens -> {b(is_valid_serialization(big))}, "
          f"one more # -> {b(is_valid_serialization(extra))}")


main()
