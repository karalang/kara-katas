# LeetCode #2315: Count Asterisks -- the Python mirror of the ★ arm. One
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


def text(n, bars, stars):
    s = []
    count = 0
    for _ in range(n):
        if next_random() % bars == 0:
            s.append("|")
            count += 1
        elif next_random() % stars == 0:
            s.append("*")
        else:
            s.append(chr(ord("a") + next_random() % 26))
    if count % 2 == 1:
        s.append("|")
    return "".join(s)


cases = ["l|*e*et|c**o|*de|", "iamprogrammer", "yo|uar|e**|b|e***au|tifu|l", "|*|", "**", "||**||", "*|*|*|*|*"]
for s in cases:
    print(f"{s}: {count_asterisks(s)}")
print(f"999 characters: {count_asterisks(text(999, 3, 2))}")
check = 0
total = 0
for _ in range(2000):
    n = next_random() % 40 + 1
    bars = next_random() % 7 + 2
    stars = next_random() % 4 + 1
    out = count_asterisks(text(n, bars, stars))
    check = (check * 31 + out) % 1000000007
    total += out
print(f"2000 strings: checksum {check}, {total} stars in all")
