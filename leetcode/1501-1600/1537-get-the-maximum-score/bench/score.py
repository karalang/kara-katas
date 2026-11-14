# LeetCode #1537: Get the Maximum Score -- bench: the ★ arm over 100
# random pairs of arrays built from 100000 values each, steps up to 50,
# built once and answered 20 times. Python mirror of score.kara.


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


pairs = [arrays(100000, 50) for _ in range(100)]
check = 0
for _ in range(20):
    for first, second in pairs:
        check = mix(check, max_sum(first, second))
print(f"20 passes over 100 pairs of 100000 values: checksum {check}")
