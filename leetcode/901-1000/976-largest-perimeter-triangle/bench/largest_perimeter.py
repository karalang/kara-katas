# Benchmark: LeetCode #976 Largest Perimeter Triangle -- the ★ arm, sort
# and scan from the top, on 20 lists of 10000 random lengths. Mirrors
# largest_perimeter.kara, .rs, .c and go-seq/.


def largest_perimeter(nums):
    a = sorted(nums)
    i = len(a) - 1
    while i >= 2:
        if a[i - 2] + a[i - 1] > a[i]:
            return a[i - 2] + a[i - 1] + a[i]
        i -= 1
    return 0


seed = 976


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds, count = 50, 20
    lists = []
    for _ in range(count):
        nums = []
        for _ in range(10000):
            hi = next_random()
            nums.append(1 + (hi * 32768 + next_random()) % 1000000)
        lists.append(nums)
    total = check = 0
    for r in range(rounds):
        for i in range(count):
            p = largest_perimeter(lists[(r + i) % count])
            total += p
            check = (check * 31 + p) % 1000000007
    print(f"{rounds} rounds over {count} lists of 10000 lengths: "
          f"perimeters total {total}, checksum {check}")


main()
