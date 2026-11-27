# LeetCode #1806: Minimum Number of Operations to Reinitialize a
# Permutation -- the bench in Python: the ★ arm over 3000 calls, each n an
# even number to 1000 drawn from the checksum so far.


def reinitialize_permutation(n):
    start = list(range(n))
    perm = start[:]
    ops = 0
    while True:
        arr = [0] * n
        for i in range(n):
            arr[i] = perm[i // 2] if i % 2 == 0 else perm[n // 2 + (i - 1) // 2]
        perm = arr
        ops += 1
        if perm == start:
            return ops


def main():
    check = 0
    for call in range(3000):
        n = 2 * (1 + (check + call) % 500)
        check = (check * 31 + reinitialize_permutation(n)) % 1000000007
    print(f"3000 calls of even n to 1000: checksum {check}")


main()
