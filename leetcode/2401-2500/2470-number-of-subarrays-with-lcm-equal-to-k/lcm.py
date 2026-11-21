def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)


def subarray_lcm(nums, k):
    n = len(nums)
    count = 0
    for start in range(n):
        lcm = 1
        for end in range(start, n):
            lcm = lcm // gcd(lcm, nums[end]) * nums[end]
            if k % lcm != 0:
                break
            if lcm == k:
                count += 1
    return count


# ---- test harness ---------------------------------------------------------

seed = 2470


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_nums(n, k):
    divisors = [d for d in range(1, k + 1) if k % d == 0]
    out = []
    for _ in range(n):
        if next_random() % 8 == 0:
            out.append(1 + next_random() % 1000)
        else:
            out.append(divisors[next_random() % len(divisors)])
    return out


def show(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def main():
    cases = [
        ([3, 6, 2, 7, 1], 6),
        ([3], 2),
        ([1, 1, 1, 1], 1),
        ([4, 9, 25], 7),
        ([7, 1, 7, 14, 7], 7),
        ([8, 1, 3, 5, 1, 7, 8, 105, 840, 2], 840),
    ]
    for nums, k in cases:
        print(f"{show(nums)}, k {k} -> {subarray_lcm(nums, k)}")
    same = [997] * 1000
    print(f"1000 of 997, k 997 -> {subarray_lcm(same, 997)}")
    print(f"1000 divisors of 840 -> {subarray_lcm(random_nums(1000, 840), 840)}")
    print(f"1000 divisors of 720 -> {subarray_lcm(random_nums(1000, 720), 720)}")
    any_nums = [1 + next_random() % 12 for _ in range(1000)]
    print(f"1000 of 1 to 12, k 12 -> {subarray_lcm(any_nums, 12)}")
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 30
        k = 1 + next_random() % 1000
        nums = random_nums(n, k)
        check = (check * 31 + subarray_lcm(nums, k)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
