# Benchmark: LeetCode #969 Pancake Sorting -- the ★ arm, the largest
# pancake to the bottom one at a time, on 200 random stacks of 100
# pancakes. Mirrors pancake_sort.kara, .c, .rs and go-seq/.


def flip(a, k):
    i, j = 0, k - 1
    while i < j:
        a[i], a[j] = a[j], a[i]
        i += 1
        j -= 1


def pancake_sort(arr):
    a = list(arr)
    flips = []
    size = len(a)
    while size > 1:
        i = 0
        while a[i] != size:
            i += 1
        if i != size - 1:
            if i != 0:
                flip(a, i + 1)
                flips.append(i + 1)
            flip(a, size)
            flips.append(size)
        size -= 1
    return flips


seed = 969


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_permutation(n):
    a = list(range(1, n + 1))
    i = n - 1
    while i > 0:
        j = next_random() % (i + 1)
        a[i], a[j] = a[j], a[i]
        i -= 1
    return a


def main():
    rounds, count = 100, 200
    stacks = [random_permutation(100) for _ in range(count)]
    flips = check = 0
    for r in range(rounds):
        for s in range(count):
            for k in pancake_sort(stacks[(r + s) % count]):
                flips += 1
                check = (check * 131 + k) % 1000000007
    print(f"{rounds} rounds over {count} stacks of 100 pancakes: {flips} flips, checksum {check}")


main()
