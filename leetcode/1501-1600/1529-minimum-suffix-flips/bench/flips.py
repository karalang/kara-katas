# LeetCode #1529: Minimum Suffix Flips -- bench: the ★ arm over 200 random
# strings of 1 to 100000 bits, built once and answered 50 times.


def min_flips(target):
    flips = 0
    prev = "0"
    for c in target:
        if c != prev:
            flips += 1
            prev = c
    return flips


seed = 1529


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    targets = []
    for _ in range(200):
        n = (next_random() * 32768 + next_random()) % 100000 + 1
        ones = next_random() % 9 + 1
        targets.append("".join("1" if next_random() % 10 < ones else "0" for _ in range(n)))
    check = 0
    for _ in range(50):
        for target in targets:
            check = mix(check, min_flips(target))
    print(f"50 passes over 200 strings of up to 100000 bits: checksum {check}")


main()
