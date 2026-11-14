# LeetCode #1546: Maximum Number of Non-Overlapping Subarrays With Sum Equals
# Target -- Python mirror of subarrays.kara (the ★ arm, greedy with a set of
# prefix sums cleared at each cut); its output is byte-identical.


def max_non_overlapping(nums, target):
    seen = {0}
    total = 0
    count = 0
    for x in nums:
        total += x
        if total - target in seen:
            count += 1
            seen = {0}
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


def batch(count, most, spread):
    check = 0
    total = 0
    for _ in range(count):
        a = next_random()
        n = (a * 32768 + next_random()) % most + 1
        nums = [next_random() % (2 * spread + 1) - spread for _ in range(n)]
        target = next_random() % (4 * spread + 1) - 2 * spread
        answer = max_non_overlapping(nums, target)
        total += answer
        check = mix(check, answer)
    print(f"{count} arrays of up to {most} values in -{spread}..{spread}: {total} subarrays, checksum {check}")


def show(v):
    return "[" + ", ".join(str(x) for x in v) + "]"


def main():
    examples = [
        ([1, 1, 1, 1, 1], 2),
        ([-1, 3, 5, 1, 4, 2, -9], 6),
        ([-2, 6, 6, 3, 5, 4, 1, 2, 8], 10),
        ([0, 0, 0], 0),
        ([5], 5),
        ([5], 4),
        ([1, -1, 1, -1], 0),
        ([3, -3, 3], 3),
    ]
    for nums, target in examples:
        print(f"{show(nums)}, target {target} -> {max_non_overlapping(nums, target)}")
    batch(3000, 12, 3)
    batch(300, 1000, 5)
    batch(30, 100000, 10)


main()
