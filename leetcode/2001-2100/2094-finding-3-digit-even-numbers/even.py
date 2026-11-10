# LeetCode #2094: Finding 3-Digit Even Numbers -- Python mirror of the ★
# arm (even.kara): count each digit, then keep each even number from 100
# to 998 whose three digits the counts can pay for.


def find_even_numbers(digits):
    have = [0] * 10
    for d in digits:
        have[d] += 1
    found = []
    for x in range(100, 1000, 2):
        need = [0] * 10
        need[x // 100] += 1
        need[x // 10 % 10] += 1
        need[x % 10] += 1
        if all(need[d] <= have[d] for d in range(10)):
            found.append(x)
    return found


# ---- test harness -----------------------------------------------------------

seed = 2094


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [
        [2, 1, 3, 0],
        [2, 2, 8, 8, 2],
        [3, 7, 5],
        [0, 0, 0],
        [1, 0, 0],
        [8, 8, 8, 8],
        [4, 0, 4, 1, 0],
    ]
    for digits in examples:
        print(f"{show(digits)} -> {show(find_even_numbers(digits))}")
    count = 0
    check = 0
    for _ in range(2000):
        length = next_random() % 10 + 3
        top = [10, 5, 3][next_random() % 3]
        digits = [next_random() % top for _ in range(length)]
        got = find_even_numbers(digits)
        count += len(got)
        for x in got:
            check = (check * 31 + x) % 1000000007
        check = (check * 31 + 1000) % 1000000007
    print(f"2000 lists: {count} numbers, checksum {check}")
    sevens = [7] * 100
    sevens[next_random() % 50] = 4
    sevens[next_random() % 50 + 50] = 0
    alld = [i % 10 for i in range(100)]
    print(f"98 sevens, a 4 and a 0 -> {show(find_even_numbers(sevens))}")
    a = find_even_numbers(alld)
    print(f"every digit ten times: {len(a)} numbers, from {a[0]} to {a[-1]}")


main()
