# Benchmark for #678: the range of open counts, the ★ arm.


def check_valid_string(s):
    low = 0
    high = 0
    for c in s:
        if c == '(':
            low += 1
            high += 1
        elif c == ')':
            low -= 1
            high -= 1
        else:
            low -= 1
            high += 1
        if high < 0:
            return False
        if low < 0:
            low = 0
    return low == 0


seed = 678


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(c):
    s = []
    if c % 3 == 0:
        n = 1 + next_random() % 100
        for _ in range(n):
            s.append("()*"[next_random() % 3])
        return "".join(s)
    left = 1 + next_random() % 50
    opened = 0
    b = []
    while left > 0 or opened > 0:
        if left > 0 and (opened == 0 or next_random() % 2 == 0):
            b.append('(')
            opened += 1
            left -= 1
        else:
            b.append(')')
            opened -= 1
    stars = next_random() % 4
    changes = next_random() % 3
    for ch in b:
        r = next_random() % 10
        if r < stars:
            s.append('*')
        elif r == 9 and next_random() % 3 < changes:
            s.append(')' if ch == '(' else '(')
        else:
            s.append(ch)
    return "".join(s)


def main():
    count = 20000
    rounds = 100
    strings = [random_string(c) for c in range(count)]
    total = 0
    valid = 0
    for r in range(rounds):
        for i in range(count):
            k = (i * 7919 + r * 104729) % count
            n = len(strings[k])
            if check_valid_string(strings[k]):
                valid += 1
                total = (total * 31 + n) % 1000000007
            else:
                total = (total * 31 + 1000 + n) % 1000000007
    print(f"{rounds} rounds of {count} strings: {valid} valid, checksum {total}")


main()
