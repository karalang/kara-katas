# LeetCode #1537: Get the Maximum Score -- Python mirror of score.kara
# (two pointers, the best sums ending on each array); output
# byte-identical.


def max_sum(nums1, nums2):
    n, m = len(nums1), len(nums2)
    i = j = a = b = 0
    while i < n or j < m:
        if i < n and (j == m or nums1[i] < nums2[j]):
            a += nums1[i]
            i += 1
        elif j < m and (i == n or nums2[j] < nums1[i]):
            b += nums2[j]
            j += 1
        else:
            a = b = max(a, b) + nums1[i]
            i += 1
            j += 1
    return max(a, b) % 1000000007


seed = 1537


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def arrays(count, gap):
    first, second = [], []
    value = 0
    both = next_random() % 30 + 1
    for _ in range(count):
        value += next_random() % gap + 1
        roll = next_random() % 100
        if roll < both:
            first.append(value)
            second.append(value)
        elif roll < 50 + both // 2:
            first.append(value)
        else:
            second.append(value)
    if not first:
        first.append(value + 1)
    if not second:
        second.append(value + 2)
    return first, second


def batch(count, most, gap):
    check = 0
    for _ in range(count):
        hi = next_random()
        n = (hi * 32768 + next_random()) % most + 1
        first, second = arrays(n, gap)
        check = mix(check, max_sum(first, second))
    print(f"{count} pairs of up to {most} values, steps up to {gap}: checksum {check}")


def show(v):
    return "[" + ", ".join(map(str, v)) + "]"


for first, second in [([2, 4, 5, 8, 10], [4, 6, 8, 9]), ([1, 3, 5, 7, 9], [3, 5, 100]),
                      ([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]), ([7], [7]), ([1, 10], [5])]:
    print(f"{show(first)}, {show(second)} -> {max_sum(first, second)}")
big = [10000000 - i * 3 for i in range(100000)][::-1]
print(f"100000 shared values near 10^7 -> {max_sum(big, big)}")
batch(3000, 12, 5)
batch(300, 1000, 100)
batch(30, 100000, 50)
