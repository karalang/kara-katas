# LeetCode #921: Minimum Add to Make Parentheses Valid -- bench: one count
# of the open parentheses. Mirrors min_add_to_make_valid.kara.


def min_add_to_make_valid(s):
    open_ = 0
    added = 0
    for c in s:
        if c == "(":
            open_ += 1
        elif open_ > 0:
            open_ -= 1
        else:
            added += 1
    return added + open_


seed = 921


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count, n = 100, 1000, 1000
    # count strings of n parentheses, built once, leaning from ')' to '('
    strings = []
    for i in range(count):
        lean = 30 + i % 41
        strings.append("".join("(" if next_random() % 100 < lean else ")" for _ in range(n)))
    total = 0
    check = 0
    for r in range(rounds):
        # each round visits every string, starting from a different one
        for i in range(count):
            a = min_add_to_make_valid(strings[(r + i) % count])
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over {count} strings of {n}: answers summing to {total}, checksum {check}")


main()
