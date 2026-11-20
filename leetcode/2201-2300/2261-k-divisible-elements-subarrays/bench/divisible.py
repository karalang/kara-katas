# LeetCode #2261: K Divisible Elements Subarrays -- Python mirror of the
# ★ arm (divisible.kara) on the bench workload: from every start the
# subarray grows until more than k of its elements are divisible by p,
# each one put into a set as a tuple. Output is byte-identical to
# divisible.kara.


def count_distinct(nums, k, p):
    seen = set()
    for start in range(len(nums)):
        divisible = 0
        run = []
        for end in range(start, len(nums)):
            if nums[end] % p == 0:
                divisible += 1
            if divisible > k:
                break
            run.append(nums[end])
            seen.add(tuple(run))
    return len(seen)


# ---- bench harness ---------------------------------------------------------

seed = 2261


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for _ in range(40):
        nums = [next_random() % 200 + 1 for _ in range(200)]
        p = next_random() % 8 + 2
        k = next_random() % 196 + 5
        check = (check * 31 + count_distinct(nums, k, p)) % 1000000007
    print(f"40 arrays of 200: checksum {check}")


main()
