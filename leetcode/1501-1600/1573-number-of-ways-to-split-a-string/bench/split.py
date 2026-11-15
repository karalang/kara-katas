# LeetCode #1573: Number of Ways to Split a String -- bench: the ★ arm (the
# two gaps between the ones multiplied) over 20 strings of 500000
# characters, each with its own odds of a '1' from 1 in 1 to 1 in 1000,
# built once; then 10 rounds answering all 20, 200 answers.


def num_ways(s):
    m = 1000000007
    ones = [i for i, c in enumerate(s) if c == "1"]
    n = len(s)
    t = len(ones)
    if t == 0:
        return (n - 1) * (n - 2) // 2 % m
    if t % 3 != 0:
        return 0
    k = t // 3
    return (ones[k] - ones[k - 1]) * (ones[2 * k] - ones[2 * k - 1]) % m


seed = 1573


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 500000
    strings = []
    for _ in range(20):
        odds = next_random() % 1000 + 1
        strings.append("".join("1" if next_random() % odds == 0 else "0" for _ in range(n)))
    check = 0
    total = 0
    for _ in range(10):
        for s in strings:
            ways = num_ways(s)
            total += ways
            check = mix(check, ways)
    print(f"200 answers over 20 strings of {n} characters: ways total {total}, checksum {check}")


main()
