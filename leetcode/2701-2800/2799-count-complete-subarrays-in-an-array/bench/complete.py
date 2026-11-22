# LeetCode #2799: Count Complete Subarrays in an Array -- the bench in
# Python: the ★ arm over 2000 arrays of 1000 numbers, half from 1 to 2000
# and half from 1 to 20, all drawn first, then each answered 20 times.


def count_complete_subarrays(nums):
    d = len(set(nums))
    counts = {}
    start = 0
    complete = 0
    for v in nums:
        counts[v] = counts.get(v, 0) + 1
        while len(counts) == d:
            first = nums[start]
            held = counts[first]
            if held == 1:
                break
            counts[first] = held - 1
            start += 1
        if len(counts) == d:
            complete += start + 1
    return complete


seed = 2799


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    a = next_random()
    return a * 32768 + next_random()


def main():
    count = 2000
    rounds = 20
    cases = []
    for c in range(count):
        top = 2000 if c % 2 == 0 else 20
        cases.append([wide() % top + 1 for _ in range(1000)])
    total = 0
    check = 0
    for r in range(rounds):
        for nums in cases:
            a = count_complete_subarrays(nums)
            total += a
            check = (check * 31 + a + r) % 1000000007
    print(f"{count} arrays of 1000, {rounds} rounds: complete sum to {total}, checksum {check}")


main()
