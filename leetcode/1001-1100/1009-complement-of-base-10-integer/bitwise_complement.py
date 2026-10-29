# LeetCode #1009: Complement of Base 10 Integer -- an all-ones mask.
# Mirrors bitwise_complement.kara line for line.


def bitwise_complement(n):
    mask = 1
    while mask < n:
        mask = mask * 2 + 1
    return mask ^ n


seed = 1009


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    examples = [5, 7, 10, 0, 1, 2, 536870912, 536870911, 999999999]
    for n in examples:
        print(f"n = {n} -> {bitwise_complement(n)}")
    parts = [str(bitwise_complement(n)) for n in range(33)]
    print(f"0..32 -> {' '.join(parts)}")
    total = 0
    check = 0
    for n in range(100001):
        c = bitwise_complement(n)
        total += c
        check = (check * 31 + c) % 1000000007
    print(f"every n up to 100000: complements sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(20000):
        bits = 1 + next_random() % 30
        n = ((next_random() * 32768 + next_random()) % (1 << bits)) % 1000000000
        c = bitwise_complement(n)
        total += c
        check = (check * 31 + c) % 1000000007
    print(f"20000 random n: complements sum to {total}, checksum {check}")


main()
