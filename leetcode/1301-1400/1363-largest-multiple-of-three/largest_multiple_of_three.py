# LeetCode #1363: Largest Multiple of Three -- Python mirror of the ★ arm:
# the digits counted, the sum's residue r put right by dropping the
# smallest digit of residue r, or the two smallest of residue 3 - r, and
# the rest written from 9 down.


def largest_multiple_of_three(digits):
    count = [0] * 10
    total = 0
    for d in digits:
        count[d] += 1
        total += d
    r = total % 3
    if r != 0:
        dropped = False
        for d in (r, r + 3, r + 6):
            if count[d] > 0:
                count[d] -= 1
                dropped = True
                break
        left = 0 if dropped else 2
        for d in (3 - r, 6 - r, 9 - r):
            while left > 0 and count[d] > 0:
                count[d] -= 1
                left -= 1
    out = "".join(str(d) * count[d] for d in range(9, -1, -1))
    if out.startswith("0"):
        return "0"
    return out


seed = 1363


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, s):
    c = (check * 131 + len(s)) % 1000000007
    for b in s.encode():
        c = (c * 31 + b) % 1000000007
    return c


def main():
    cases = [[8, 1, 9], [8, 6, 7, 1, 0], [1], [0, 0, 0, 0, 0, 0], [2, 2], [5, 8, 9]]
    print(" ".join(f'"{largest_multiple_of_three(d)}"' for d in cases))
    long = [next_random() % 10 for _ in range(10000)]
    answer = largest_multiple_of_three(long)
    print(f"10^4 digits: {len(answer)} kept, checksum {fold(0, answer)}")
    check = 0
    empty = 0
    for _ in range(2000):
        n = 1 + next_random() % 30
        digits = [next_random() % 10 for _ in range(n)]
        answer = largest_multiple_of_three(digits)
        if answer == "":
            empty += 1
        check = fold(check, answer)
    print(f"2000 random arrays: {empty} with none, checksum {check}")


main()
