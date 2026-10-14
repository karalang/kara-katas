# Benchmark for #553: Python mirror of the ★ arm (the shape is always the
# same); see optimal_division.kara.


def optimal_division(nums):
    n = len(nums)
    out = []
    for i in range(n):
        if i > 0:
            out.append("/")
        if i == 1 and n > 2:
            out.append("(")
        out.append(str(nums[i]))
    if n > 2:
        out.append(")")
    return "".join(out)


seed = 553


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 2000
    all_a = []
    for _ in range(count):
        n = 1 + next_random() % 10
        all_a.append([2 + next_random() % 999 for _ in range(n)])
    chars = checksum = 0
    for rnd in range(500):
        for g in range(count):
            b = optimal_division(all_a[(rnd * 7 + g) % count]).encode()
            chars += len(b)
            checksum = (checksum * 31 + len(b) + b[len(b) // 2]) % 1000000007
    print(f"{count} arrays, 500 rounds each: {chars} characters, checksum {checksum}")


main()
