# LeetCode #1567: Maximum Length of Subarray With Positive Product --
# bench: the ★ arm over 20 arrays of 200000 values, built once, each
# value 0 one time in 5000 and otherwise of 1 to 1000, negative one time in
# three; 20 passes, each first flipping the sign of one value of every
# array.


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


seed = 1567


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 200000
    arrays = []
    for _ in range(20):
        nums = []
        for _ in range(n):
            size = next_random() % 1000 + 1
            kind = next_random()
            nums.append(0 if kind % 5000 == 0 else -size if kind % 3 == 0 else size)
        arrays.append(nums)
    check = 0
    total = 0
    for p in range(20):
        for a in range(len(arrays)):
            at = (p * 7919 + a * 104729) % n
            arrays[a][at] = -arrays[a][at]
            length = get_max_len(arrays[a])
            total += length
            check = mix(check, length)
    print(f"20 passes over 20 arrays of 200000 values: lengths sum {total}, checksum {check}")


main()
