# LeetCode #1545: Find Kth Bit in Nth Binary String -- Python mirror of
# kth_bit.kara (the ★ arm, the definition's recursion); its output is
# byte-identical.


def find_kth_bit(n, k):
    if n == 1:
        return "0"
    middle = 1 << (n - 1)
    if k == middle:
        return "1"
    if k < middle:
        return find_kth_bit(n - 1, k)
    return "1" if find_kth_bit(n - 1, (1 << n) - k) == "0" else "0"


seed = 1545


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    examples = [(3, 1), (4, 11), (1, 1), (2, 3), (2, 2), (20, 524288), (20, 1048575), (20, 1)]
    for n, k in examples:
        print(f"n = {n}, k = {k} -> {find_kth_bit(n, k)}")
    print("S4 = " + "".join(find_kth_bit(4, k) for k in range(1, 16)))
    ones = 0
    check = 0
    for k in range(1, 65536):
        bit = find_kth_bit(16, k)
        if bit == "1":
            ones += 1
        check = mix(check, 1 if bit == "1" else 0)
    print(f"every k of S16: {ones} ones, checksum {check}")
    ones = 0
    check = 0
    for _ in range(3000):
        n = next_random() % 20 + 1
        a = next_random()
        k = (a * 32768 + next_random()) % ((1 << n) - 1) + 1
        bit = find_kth_bit(n, k)
        if bit == "1":
            ones += 1
        check = mix(check, n * 2 + (1 if bit == "1" else 0))
    print(f"3000 random n and k: {ones} ones, checksum {check}")


main()
