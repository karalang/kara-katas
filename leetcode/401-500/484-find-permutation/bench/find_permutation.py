# Benchmark for #484: Python mirror of the ★ arm (1 to n, each run of Ds
# reversed); see find_permutation.kara.


def find_permutation(s):
    letters = list(s)
    n = len(letters) + 1
    perm = [i + 1 for i in range(n)]
    i = 0
    while i < len(letters):
        if letters[i] == "D":
            start = i
            while i < len(letters) and letters[i] == "D":
                i += 1
            low, high = start, i
            while low < high:
                perm[low], perm[high] = perm[high], perm[low]
                low += 1
                high -= 1
        else:
            i += 1
    return perm


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    patterns = []
    seed = [484]
    for p in range(20):
        s = []
        for _ in range(100000):
            s.append("D" if next_random(seed) % 20 < p else "I")
        patterns.append("".join(s))
    total = 0
    checksum = 0
    for _ in range(10):
        for s in patterns:
            perm = find_permutation(s)
            n = len(perm)
            total += n
            checksum = (checksum * 31 + perm[0] + perm[n // 2] * 7 + perm[n - 1] * 13) % 1000000007
    print(f"200 solves of 100000 letters: {total} numbers, checksum {checksum}")


main()
