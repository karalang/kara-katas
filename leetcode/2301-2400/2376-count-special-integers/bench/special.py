# LeetCode #2376: Count Special Integers -- the bench, the ★ arm in
# Python: the shorter numbers counted by length, then n's own length place
# by place, each place adding its smaller unused digits times the
# arrangements of the places after it.


def arrangements(free, places):
    ways = 1
    for k in range(places):
        ways *= free - k
    return ways


def count_special_numbers(n):
    digits = [int(c) for c in str(n)]
    length = len(digits)
    count = 0
    for l in range(1, length):
        count += 9 * arrangements(9, l - 1)
    used = [False] * 10
    for i in range(length):
        low = 1 if i == 0 else 0
        for d in range(low, digits[i]):
            if not used[d]:
                count += arrangements(9 - i, length - 1 - i)
        if used[digits[i]]:
            return count
        used[digits[i]] = True
    return count + 1


seed = 2376


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    # 10^5 values of 1 to 10 digits, at most 2 * 10^9
    values = []
    for _ in range(100000):
        digits = 1 + next_random() % 10
        top = 10 ** digits
        high = next_random()
        r = high * 32768 + next_random()
        values.append(1 + r % (min(top, 2000000001) - 1))
    check = 0
    for p in range(100):
        for v in values:
            check = (check * 31 + count_special_numbers(v) + p) % 1000000007
    print(f"100 passes over 10^5 values: checksum {check}")


main()
