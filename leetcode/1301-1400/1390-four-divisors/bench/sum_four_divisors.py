# LeetCode #1390 bench, Python mirror of the ★ arm.


def sum_four_divisors(nums):
    total = 0
    for v in nums:
        count = 0
        s = 0
        d = 1
        while d * d <= v and count <= 4:
            if v % d == 0:
                count += 1
                s += d
                if d * d != v:
                    count += 1
                    s += v // d
            d += 1
        if count == 4:
            total += s
    return total


seed = 1390


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    global seed
    n = 10000
    nums = []
    for _ in range(n):
        a = next_random()
        b = next_random()
        nums.append(1 + (a * 32768 + b) % 100000)
    check = 0
    for _ in range(300):
        seed = (seed + check) % 2147483648
        i = next_random() % n
        a = next_random()
        b = next_random()
        nums[i] = 1 + (a * 32768 + b) % 100000
        check = (check * 131 + sum_four_divisors(nums)) % 1000000007
    print(f"300 rounds over 10^4 values up to 10^5: checksum {check}")


main()
