# LeetCode #2261: K Divisible Elements Subarrays -- Python mirror of the
# ★ arm (divisible.kara): from every start the subarray grows until more
# than k of its elements are divisible by p, each one put into a set.
# Output is byte-identical to the Kara arms.


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


# ---- test harness ---------------------------------------------------------

seed = 2261


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    examples = [([2, 3, 3, 2, 2], 2, 2), ([1, 2, 3, 4], 4, 1), ([6], 1, 3), ([5, 5, 5, 5], 2, 5), ([1, 3, 7, 9], 1, 2), ([4, 8, 4, 8], 1, 4)]
    for nums, k, p in examples:
        print(f"{nums} k={k} p={p} -> {count_distinct(nums, k, p)}")
    check = 0
    total = 0
    for _ in range(2000):
        n = next_random() % 20 + 1
        nums = [next_random() % 10 + 1 for _ in range(n)]
        k = next_random() % n + 1
        p = next_random() % 10 + 1
        answer = count_distinct(nums, k, p)
        total += answer
        check = (check * 31 + answer) % 1000000007
    print(f"2000 arrays: {total} subarrays, checksum {check}")
    ones = [1] * 200
    random = [next_random() % 200 + 1 for _ in range(200)]
    ordered = list(range(1, 201))
    small = [next_random() % 3 + 1 for _ in range(200)]
    answers = [count_distinct(ones, 50, 1), count_distinct(random, 200, 7), count_distinct(ordered, 10, 2), count_distinct(small, 20, 3)]
    print(f"200 elements: {answers}")


main()
