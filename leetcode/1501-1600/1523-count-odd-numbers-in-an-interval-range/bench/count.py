# LeetCode #1523: Count Odd Numbers in an Interval Range -- bench: the ★
# arm over 2000000 random intervals within 0 to 10^9, built once and
# answered 100 times, each pass summed.


def count_odds(low, high):
    return (high + 1) // 2 - low // 2


seed = 1523


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    count = 2000000
    lows = []
    highs = []
    for _ in range(count):
        a = (next_random() * 32768 + next_random()) % 1000000001
        b = (next_random() * 32768 + next_random()) % 1000000001
        lows.append(min(a, b))
        highs.append(max(a, b))
    check = 0
    for _ in range(100):
        total = 0
        for i in range(count):
            total += count_odds(lows[i], highs[i])
        check = mix(check, total % 1000000007)
    print(f"100 passes over 2000000 intervals within 0 to 10^9: checksum {check}")


main()
