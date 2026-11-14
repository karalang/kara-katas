# LeetCode #1546: Maximum Number of Non-Overlapping Subarrays With Sum Equals
# Target -- bench: the ★ arm (greedy, a set of prefix sums cleared at each
# cut) over 100 arrays of 1 to 100000 values in -10..10, each with a target
# in -20..20, built once, each asked 5 times. Python mirror of
# subarrays.kara.


def max_non_overlapping(nums, target):
    seen = {0}
    total = 0
    count = 0
    for x in nums:
        total += x
        if total - target in seen:
            count += 1
            seen.clear()
            seen.add(0)
            total = 0
        else:
            seen.add(total)
    return count


seed = 1546


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    cases = []
    for _ in range(100):
        a = next_random()
        n = (a * 32768 + next_random()) % 100000 + 1
        nums = [next_random() % 21 - 10 for _ in range(n)]
        target = next_random() % 41 - 20
        cases.append((nums, target))
    check = 0
    total = 0
    for _ in range(5):
        for nums, target in cases:
            answer = max_non_overlapping(nums, target)
            total += answer
            check = mix(check, answer)
    print(f"5 passes over 100 arrays of up to 100000 values: {total} subarrays, checksum {check}")


main()
