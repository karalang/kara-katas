# LeetCode #921: Minimum Add to Make Parentheses Valid -- mirrors
# min_add_to_make_valid.kara (one count of the open parentheses) and its
# harness.


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


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s):
    print(f'"{s}": {min_add_to_make_valid(s)}')


def random_string(n, lean):
    return "".join("(" if next_random() % 100 < lean else ")" for _ in range(n))


def main():
    global seed
    for s in ["())", "(((", "()", ")(", "(()())", "()))((", ")))", "(()))(()", "((((", "())(()"]:
        show(s)
    seed = 921
    total = 0
    check = 0
    for r in range(500):
        n = 1 + next_random() % 1000
        s = random_string(n, 30 + r % 41)
        a = min_add_to_make_valid(s)
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"500 random strings: answers summing to {total}, checksum {check}")
    opens = "(" * 1000
    closes = ")" * 1000
    pairs = "()" * 500
    flipped = ")(" * 500
    nested = "(" * 500 + ")" * 500
    print(f"1000 '(': {min_add_to_make_valid(opens)}, 1000 ')': {min_add_to_make_valid(closes)}, \"()\" x 500: {min_add_to_make_valid(pairs)}, \")(\" x 500: {min_add_to_make_valid(flipped)}, nested 500 deep: {min_add_to_make_valid(nested)}")


main()
