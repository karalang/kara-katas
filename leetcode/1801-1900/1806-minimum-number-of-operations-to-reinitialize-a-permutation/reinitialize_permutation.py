# LeetCode #1806: Minimum Number of Operations to Reinitialize a
# Permutation -- the ★ arm in Python: the operation applied as the
# statement writes it until `perm` is back where it started.


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
    # LeetCode's three examples
    print(reinitialize_permutation(2), reinitialize_permutation(4), reinitialize_permutation(6))
    # the edges
    print(*[reinitialize_permutation(n) for n in [66, 514, 12, 14, 1000]])
    # every even n from 2 to 1000
    check = 0
    total = 0
    most = 0
    for half in range(1, 501):
        ops = reinitialize_permutation(2 * half)
        check = (check * 31 + ops) % 1000000007
        total += ops
        most = max(most, ops)
    print(f"every even n to 1000: checksum {check}, total {total}, most {most}")


main()
