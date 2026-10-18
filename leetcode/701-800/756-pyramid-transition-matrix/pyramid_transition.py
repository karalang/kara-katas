# LeetCode 756 — Pyramid Transition Matrix: Python mirror of the ★ arm
# and its harness (same depth-first search, same memo, same output).
import sys

sys.setrecursionlimit(10000)


def row_code(row):
    code = 1
    for x in row:
        code = code * 6 + x
    return code


def fill(row, i, nxt, table, dead):
    if i + 1 == len(row):
        return build(nxt, table, dead)
    options = table[row[i] * 6 + row[i + 1]]
    block = 0
    while options > 0:
        if options & 1 == 1:
            nxt.append(block)
            if fill(row, i + 1, nxt, table, dead):
                return True
            nxt.pop()
        options >>= 1
        block += 1
    return False


def build(row, table, dead):
    if len(row) == 1:
        return True
    code = row_code(row)
    if code in dead:
        return False
    nxt = []
    if fill(row, 0, nxt, table, dead):
        return True
    dead.add(code)
    return False


def pyramid_transition(bottom, allowed):
    table = [0] * 36
    for t in allowed:
        pair = (ord(t[0]) - 65) * 6 + (ord(t[1]) - 65)
        table[pair] |= 1 << (ord(t[2]) - 65)
    row = [ord(c) - 65 for c in bottom]
    return build(row, table, set())


seed = 756


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(bottom, allowed):
    answer = "true" if pyramid_transition(bottom, allowed) else "false"
    print(f"{bottom} with {len(allowed)} triples -> {answer}")


def main():
    show("BCD", ["BCC", "CDE", "CEA", "FFF"])
    show("AAAA", ["AAB", "AAC", "BCD", "BBE", "DEF"])
    show("AB", ["ABC"])
    show("AB", ["BAC"])
    show("AB", [])
    show("FFFFFF", ["FFF"])
    show("ABCDEF", ["FFF"])
    yes = 0
    check = 0
    for rnd in range(300):
        width = 2 + next_random() % 5
        bottom = "".join(chr(65 + next_random() % 6) for _ in range(width))
        count = next_random() % 60
        allowed = []
        for _ in range(count):
            allowed.append("".join(chr(65 + next_random() % 6) for _ in range(3)))
        if pyramid_transition(bottom, allowed):
            yes += 1
            check = (check * 31 + rnd) % 1000000007
    print(f"300 random pyramids: {yes} can be built, checksum {check}")


main()
