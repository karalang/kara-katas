# LeetCode #2275: Largest Combination With Bitwise AND Greater Than Zero
# -- the bench, the ★ arm.


def largest_combination(candidates):
    best = 0
    for bit in range(24):
        count = 0
        for x in candidates:
            if (x >> bit) & 1 == 1:
                count += 1
        best = max(best, count)
    return best


# ---- bench harness ---------------------------------------------------------

seed = 2275


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(100):
        candidates = []
        for _ in range(100000):
            high = next_random()
            candidates.append((high * 32768 + next_random()) % 10000000 + 1)
        check = (check * 31 + largest_combination(candidates)) % 1000000007
    print(f"100 lists of 10^5: checksum {check}")


main()
