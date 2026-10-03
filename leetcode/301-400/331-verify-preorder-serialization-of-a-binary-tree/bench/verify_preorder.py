# Benchmark workload for LeetCode #331 — Python mirror of verify_preorder.kara.
import sys

sys.setrecursionlimit(10000)

NODES = 100000
VARIANTS = 16
PUNCHES = 160
MODULUS = 1073741789

seed = 331


def nxt():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


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


def tree(n, out):
    if n == 0:
        out.append("#")
        return
    out.append(str(nxt() % 100))
    left = nxt() % n
    tree(left, out)
    tree(n - 1 - left, out)


def main():
    tokens = []
    tree(NODES, tokens)
    variants = []
    for v in range(VARIANTS):
        kind = v % 4
        hi = nxt()
        at = (hi * 32768 + nxt()) % len(tokens)
        edited = []
        for i, t in enumerate(tokens):
            if i == at and kind == 1:
                continue
            if i == at and kind == 3:
                edited.append("#")
            if i == at and kind == 2 and t == "#":
                edited.append("7")
                edited.append("#")
            edited.append(t)
        variants.append(",".join(edited))
    sink = 0
    for _ in range(PUNCHES):
        v = nxt() % VARIANTS
        answer = 1 if is_valid_serialization(variants[v]) else 0
        sink = (sink * 1000003 + answer * 64 + v) % MODULUS
    print(sink)


main()
