# LeetCode #1567: Maximum Length of Subarray With Positive Product -- the
# Python mirror of the ★ arm (positive.kara): the longest run ending here
# with a positive product and with a negative one. O(n)


def get_max_len(nums):
    positive = 0
    negative = 0
    best = 0
    for x in nums:
        if x > 0:
            positive += 1
            negative = negative + 1 if negative > 0 else 0
        elif x < 0:
            was_positive = positive
            positive = negative + 1 if negative > 0 else 0
            negative = was_positive + 1
        else:
            positive = 0
            negative = 0
        best = max(best, positive)
    return best


# ---- the harness: the same in every arm

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, zeros, top):
    check = 0
    total = 0
    for _ in range(count):
        n = (next_random() * 32768 + next_random()) % most + 1
        nums = []
        for _ in range(n):
            size = (next_random() * 32768 + next_random()) % top + 1
            kind = next_random()
            nums.append(0 if kind % zeros == 0 else -size if kind % 3 == 0 else size)
        length = get_max_len(nums)
        total += length
        check = mix(check, length)
    print(f"{count} arrays of up to {most} values: lengths sum {total}, checksum {check}")


def main():
    global seed
    examples = [
        [1, -2, -3, 4],
        [0, 1, -2, -3, -4],
        [-1, -2, -3, 0, 1],
        [-1],
        [0],
        [5],
        [-1, 2],
        [2, -1, 3, 4, 0, 5, 6, -7, 8],
        [-1000000000, -1000000000, -1000000000, -1000000000],
    ]
    for nums in examples:
        print(f"[{', '.join(map(str, nums))}] -> {get_max_len(nums)}")
    seed = 1567
    batch(3000, 10, 5, 5)
    batch(300, 1000, 50, 1000)
    batch(30, 100000, 1000, 1000000000)


main()
