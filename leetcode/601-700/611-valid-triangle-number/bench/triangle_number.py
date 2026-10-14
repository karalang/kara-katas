# Benchmark mirror for #611: the same workload and algorithm as
# triangle_number.kara (sort, then two pointers).


def triangle_number(nums):
    a = sorted(nums)
    count = 0
    for k in range(2, len(a)):
        i = 0
        j = k - 1
        while i < j:
            if a[i] + a[j] > a[k]:
                count += j - i
                j -= 1
            else:
                i += 1
    return count


seed = 611


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    arrays = 20
    rounds = 600
    every = []
    for _ in range(arrays):
        bound = 100 + step() % 901
        every.append([step() % (bound + 1) for _ in range(1000)])
    total = 0
    checksum = 0
    for r in range(rounds):
        got = triangle_number(every[(r * 7) % arrays])
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"{arrays} arrays, {rounds} rounds: {total} triangles, checksum {checksum}")


main()
