# LeetCode #2275: Largest Combination With Bitwise AND Greater Than Zero
# -- the Python mirror of the ★ arm, `combo.kara`, line for line. Its
# output is byte-identical.


def largest_combination(candidates):
    best = 0
    for bit in range(24):
        count = 0
        for x in candidates:
            if (x >> bit) & 1 == 1:
                count += 1
        best = max(best, count)
    return best


seed = 2275


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def values(n, high):
    out = []
    for _ in range(n):
        a = next_random()
        b = next_random()
        out.append((a * 32768 + b) % high + 1)
    return out


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


def main():
    examples = [
        [16, 17, 71, 62, 12, 24, 14],
        [8, 8],
        [1],
        [1, 2, 4, 8],
        [7, 7, 7],
        [10000000],
        [3, 5, 6],
    ]
    for candidates in examples:
        print(f"{show(candidates)} -> {largest_combination(candidates)}")
    check = 0
    for t in range(2000):
        n = next_random() % 40 + 1
        candidates = values(n, [15, 1000, 10000000][t % 3])
        check = (check * 31 + largest_combination(candidates)) % 1000000007
    print(f"2000 lists: checksum {check}")
    rand = values(100000, 10000000)
    every = list(range(1, 100001))
    powers = [1 << (i % 24) for i in range(100000)]
    answers = [largest_combination(rand), largest_combination(every), largest_combination(powers)]
    print(f"10^5 values: {show(answers)}")


main()
