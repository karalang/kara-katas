# LeetCode #1375: Number of Times Binary String Is Prefix-Aligned --
# Python mirror of the ★ arm: after step i the string is aligned exactly
# when the largest bit flipped so far is i.

seed = 1375


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def num_times_all_blue(flips):
    largest = 0
    aligned = 0
    for i, f in enumerate(flips):
        largest = max(largest, f)
        if largest == i + 1:
            aligned += 1
    return aligned


def shuffled(n, block):
    flips = list(range(1, n + 1))
    start = 0
    while start < n:
        end = min(start + block, n)
        for i in range(end - 1, start, -1):
            j = start + next_random() % (i - start + 1)
            flips[i], flips[j] = flips[j], flips[i]
        start = end
    return flips


def main():
    n = 50000
    orders = [[3, 2, 4, 1, 5], [4, 1, 2, 3], list(range(1, n + 1)), list(range(n, 0, -1))]
    print(" ".join(str(num_times_all_blue(f)) for f in orders))
    total = 0
    check = 0
    for k in range(2000):
        n = 1 + next_random() % 300
        block = n if k % 4 == 0 else 2 + next_random() % 7
        got = num_times_all_blue(shuffled(n, block))
        total += got
        check = (check * 131 + got) % 1000000007
    print(f"2000 random orders: aligned {total} times, checksum {check}")


main()
