# LeetCode #976: Largest Perimeter Triangle -- Python mirror of
# largest_perimeter.kara.


def largest_perimeter(nums):
    a = sorted(nums)
    i = len(a) - 1
    while i >= 2:
        if a[i - 2] + a[i - 1] > a[i]:
            return a[i - 2] + a[i - 1] + a[i]
        i -= 1
    return 0


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, top):
    out = []
    for _ in range(n):
        hi = next_random()
        out.append(1 + (hi * 32768 + next_random()) % top)
    return out


def main():
    global seed
    fib = [1, 1]
    while len(fib) < 30:
        fib.append(fib[-1] + fib[-2])
    cases = [
        [2, 1, 2],
        [1, 2, 1, 10],
        [3, 2, 3, 4],
        [3, 6, 2, 3],
        [1, 1, 1],
        [1, 2, 3],
        [1000000, 1000000, 1000000],
        [1000000, 1, 1, 999999, 2],
        list(fib),
        fib + [2, 2, 3],
    ]
    for nums in cases:
        print(f"{len(nums)} lengths from {nums[0]}: {largest_perimeter(nums)}")
    seed = 976
    for count, most, top in [(300, 12, 10), (3000, 60, 1000), (4, 10000, 1000000)]:
        total = check = 0
        for _ in range(count):
            n = most if most == 10000 else 3 + next_random() % (most - 2)
            p = largest_perimeter(random_nums(n, top))
            total += p
            check = (check * 31 + p) % 1000000007
        print(f"{count} random cases of up to {most} lengths: "
              f"perimeters total {total}, checksum {check}")


main()
