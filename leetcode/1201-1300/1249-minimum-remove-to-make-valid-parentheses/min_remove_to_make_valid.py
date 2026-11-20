# LeetCode #1249: Minimum Remove to Make Valid Parentheses -- mirrors
# min_remove_to_make_valid.kara.


def min_remove_to_make_valid(s):
    keep = [True] * len(s)
    open_at = []
    for i, c in enumerate(s):
        if c == "(":
            open_at.append(i)
        elif c == ")":
            if open_at:
                open_at.pop()
            else:
                keep[i] = False
    for i in open_at:
        keep[i] = False
    return "".join(c for i, c in enumerate(s) if keep[i])


seed = 1249


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, percent, lean):
    out = []
    for _ in range(n):
        r = next_random() % 100
        if r < percent:
            if lean == 0:
                is_open = next_random() % 2 == 0
            elif lean == 1:
                is_open = next_random() % 5 < 3
            else:
                is_open = next_random() % 5 < 2
            out.append("(" if is_open else ")")
        else:
            out.append("abcde"[next_random() % 5])
    return "".join(out)


def valid_removal(s, kept):
    open_count = 0
    for c in kept:
        if c == "(":
            open_count += 1
        elif c == ")":
            if open_count == 0:
                return False
            open_count -= 1
    rest = iter(s)
    for c in kept:
        if not any(r == c for r in rest):
            return False

    def letters(t):
        return sum(1 for c in t if c not in "()")

    return open_count == 0 and letters(s) == letters(kept)


def main():
    a = min_remove_to_make_valid("lee(t(c)o)de)")
    b = min_remove_to_make_valid("a)b(c)d")
    c = min_remove_to_make_valid("))((")
    print(f"{a} {b} [{c}]")
    removed = 0
    invalid = 0
    check = 0
    for t in range(1000):
        n = next_random() % 2000 + 1
        percent = next_random() % 101
        s = random_text(n, percent, t % 3)
        kept = min_remove_to_make_valid(s)
        if not valid_removal(s, kept):
            invalid += 1
        removed += n - len(kept)
        check = (check * 131 + n - len(kept)) % 1000000007
    print(f"1000 random strings: {removed} removed, {invalid} invalid, checksum {check}")
    deep = "(" * 50000 + ")" * 50001
    noise = random_text(100000, 100, 0)
    x = min_remove_to_make_valid(deep)
    y = min_remove_to_make_valid(noise)
    fine = "true" if valid_removal(deep, x) and valid_removal(noise, y) else "false"
    print(f"100000 characters: nested keeps {len(x)}, random keeps {len(y)}, valid {fine}")


main()
