# LeetCode #2315: Count Asterisks -- the bench, the ★ arm in Python. One
# pass with a flag: each `|` flips whether the walk is inside a pair, and
# a `*` counts only outside one.

seed = 2315


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def count_asterisks(s):
    inside = False
    count = 0
    for c in s:
        if c == "|":
            inside = not inside
        elif c == "*" and not inside:
            count += 1
    return count


strings = []
for _ in range(1000):
    bars = next_random() % 8 + 2
    s = []
    count = 0
    for _ in range(999):
        if next_random() % bars == 0:
            s.append("|")
            count += 1
        elif next_random() % 2 == 0:
            s.append("*")
        else:
            s.append("a")
    s.append("|" if count % 2 == 1 else "a")
    strings.append("".join(s))
check = 0
for p in range(100):
    for a in range(1000):
        check = (check * 31 + count_asterisks(strings[(7 * a + p) % 1000])) % 1000000007
print(f"100 passes over 1000 strings of 1000 characters: checksum {check}")
