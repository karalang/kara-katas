# LeetCode #484: Find Permutation -- mirror of find_permutation.kara (the
# ★ arm).


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


def show(s):
    print(f"'{s}' -> [{', '.join(str(x) for x in find_permutation(s))}]")


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    for s in ["I", "DI", "D", "DDDD", "IIII", "DIDID", "IDDIIDDDI", "DDIDDDIIDD"]:
        show(s)
    count = 300
    seed = [484]
    total = 0
    checksum = 0
    for c in range(count):
        s = []
        size = 1 + next_random(seed) % 40
        for _ in range(size):
            if next_random(seed) % 4 <= c % 3:
                s.append("D")
            else:
                s.append("I")
        for x in find_permutation("".join(s)):
            total += 1
            checksum = (checksum * 31 + x) % 1000000007
    print(f"{count} random patterns: {total} numbers, checksum {checksum}")


main()
