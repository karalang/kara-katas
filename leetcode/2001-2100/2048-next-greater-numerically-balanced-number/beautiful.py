# LeetCode #2048: Next Greater Numerically Balanced Number -- Python mirror
# of the ★ arm (beautiful.kara): count upward from n + 1 and test each
# number's digit counts. Output is byte-identical to the Kāra arms.


def is_balanced(x):
    counts = [0] * 10
    while x > 0:
        counts[x % 10] += 1
        x //= 10
    return all(counts[d] == 0 or counts[d] == d for d in range(10))


def next_beautiful_number(n):
    x = n + 1
    while not is_balanced(x):
        x += 1
    return x


# ---- test harness ---------------------------------------------------------

seed = 2048


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    for n in [1, 1000, 3000, 0, 22, 1224443, 1000000, 666665, 122333, 4444]:
        print(f"{n} -> {next_beautiful_number(n)}")
    total = check = 0
    for _ in range(300):
        n = (next_random() * 32768 + next_random()) % 600000
        x = next_beautiful_number(n)
        total += x
        check = (check * 31 + x) % 1000000007
    print(f"300 values below 600000: sum {total}, checksum {check}")
    total = check = 0
    for n in [666666, 999999, 1000000]:
        x = next_beautiful_number(n)
        total += x
        check = (check * 31 + x) % 1000000007
    print(f"3 values far from the next: sum {total}, checksum {check}")


main()
