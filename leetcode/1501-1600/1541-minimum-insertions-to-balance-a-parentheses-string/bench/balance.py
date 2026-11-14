# LeetCode #1541: Minimum Insertions to Balance a Parentheses String --
# bench: the ★ arm (one pass keeping the ')' still wanted) over 100 strings
# of 1 to 100000 parentheses, built once, each asked 10 times. Python mirror
# of balance.kara.


def min_insertions(s):
    inserted = 0
    need = 0
    for c in s:
        if c == "(":
            if need % 2 == 1:
                inserted += 1
                need -= 1
            need += 2
        else:
            need -= 1
            if need < 0:
                inserted += 1
                need = 1
    return inserted + need


seed = 1541


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    strings = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 100000 + 1
        chance = next_random() % 101
        strings.append("".join("(" if next_random() % 100 < chance else ")" for _ in range(n)))
    check = 0
    for _ in range(10):
        for s in strings:
            check = mix(check, min_insertions(s))
    print(f"10 passes over 100 strings of up to 100000 parentheses: checksum {check}")


main()
