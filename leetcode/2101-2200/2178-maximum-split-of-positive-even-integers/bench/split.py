# LeetCode #2178: Maximum Split of Positive Even Integers -- the
# benchmark's Python mirror of split.kara.


def maximum_even_split(final_sum):
    parts = []
    if final_sum % 2 != 0:
        return parts
    left = final_sum
    nxt = 2
    while left >= nxt:
        parts.append(nxt)
        left -= nxt
        nxt += 2
    parts[-1] += left
    return parts


seed = 2178


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    parts_in_all = 0
    check = 0
    for _ in range(400):
        a = next_random()
        b = next_random()
        c = next_random()
        final_sum = ((a * 32768 + b) * 32768 + c) % 10000000000 + 1
        parts = maximum_even_split(final_sum)
        parts_in_all += len(parts)
        for p in parts:
            check = (check * 31 + p) % 1000000007
    print(f"400 solves: {parts_in_all} parts, checksum {check}")


main()
