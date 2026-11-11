# LeetCode #2116: Check if a Parentheses String Can Be Valid -- Python
# mirror of valid.kara, the two greedy passes; same harness, same output.


def can_be_valid(s, locked):
    n = len(s)
    if n % 2 == 1:
        return False
    s = s.encode()
    locked = locked.encode()
    open_ = 0
    for i in range(n):
        if s[i] == ord("(") or locked[i] == ord("0"):
            open_ += 1
        else:
            open_ -= 1
            if open_ < 0:
                return False
    close = 0
    for i in reversed(range(n)):
        if s[i] == ord(")") or locked[i] == ord("0"):
            close += 1
        else:
            close -= 1
            if close < 0:
                return False
    return True


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(b):
    return "true" if b else "false"


def main():
    examples = [
        ("))()))", "010100"),
        ("()()", "0000"),
        (")", "0"),
        (")(", "11"),
        ("((((", "0000"),
        ("()((", "1110"),
        ("(()", "000"),
    ]
    for s, locked in examples:
        print(f"{s} {locked} -> {show(can_be_valid(s, locked))}")
    seed = [2116]
    valid = 0
    check = 0
    for _ in range(4000):
        n = next_random(seed) % 24 + 1
        s = ""
        locked = ""
        for _ in range(n):
            s += "(" if next_random(seed) % 2 == 0 else ")"
            locked += "0" if next_random(seed) % 2 == 0 else "1"
        got = can_be_valid(s, locked)
        if got:
            valid += 1
        check = (check * 31 + (n if got else 1)) % 1000000007
    print(f"4000 strings: {valid} can be valid, checksum {check}")
    s = ")" * 100000
    half = "0" * 50000 + "1" * 50000
    short = "0" * 49999 + "1" * 50001
    print(f"half unlocked -> {show(can_be_valid(s, half))}")
    print(f"one short -> {show(can_be_valid(s, short))}")


main()
