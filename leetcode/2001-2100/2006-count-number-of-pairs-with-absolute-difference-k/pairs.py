# LeetCode #2006: Count Number of Pairs With Absolute Difference K -- the
# mirror of the ★ arm, pairs.kara; its output is byte-identical.


def count_k_difference(nums, k):
    seen = [0] * 101
    pairs = 0
    for x in nums:
        if x - k >= 1:
            pairs += seen[x - k]
        if x + k <= 100:
            pairs += seen[x + k]
        seen[x] += 1
    return pairs


seed = 2006


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, answer):
    return (check * 31 + answer) % 1000000007


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    # LeetCode's three examples, then a few more
    examples = [
        ([1, 2, 2, 1], 1),
        ([1, 3], 3),
        ([3, 2, 1, 5, 4], 2),
        ([7], 1),
        ([5, 5, 5, 5], 1),
        ([1, 100, 1, 100], 99),
        ([4, 6, 4, 6, 8, 2], 2),
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3),
    ]
    for nums, k in examples:
        print(f"{show(nums)} k = {k} -> {count_k_difference(nums, k)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 30 + 1
        top = next_random() % 10 + 1
        k = next_random() % 5 + 1
        nums = [next_random() % top + 1 for _ in range(n)]
        answer = count_k_difference(nums, k)
        total += answer
        check = mix(check, answer)
    print(f"3000 arrays of 1 to 30 values up to 10: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(50):
        k = next_random() % 99 + 1
        nums = [next_random() % 100 + 1 for _ in range(200)]
        answer = count_k_difference(nums, k)
        total += answer
        check = mix(check, answer)
    print(f"50 arrays of 200 values up to 100: sum {total}, checksum {check}")


main()
