# LeetCode #2106: Maximum Fruits Harvested After at Most K Steps -- bench,
# Python mirror of harvest.kara.


def steps(l, r, start):
    if l >= start:
        return r - start
    if r <= start:
        return start - l
    return min(2 * (start - l) + (r - start), (start - l) + 2 * (r - start))


def max_total_fruits(fruits, start, k):
    left = 0
    total = 0
    best = 0
    for right in range(len(fruits)):
        total += fruits[right][1]
        while left <= right and steps(fruits[left][0], fruits[right][0], start) > k:
            total -= fruits[left][1]
            left += 1
        best = max(best, total)
    return best


seed = 2106


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide_random():
    hi = next_random()
    return hi * 32768 + next_random()


fields = []
for _ in range(20):
    fruits = []
    for p in range(200000):
        if next_random() % 2 == 0:
            fruits.append([p, wide_random() % 10000 + 1])
    fields.append(fruits)
total = 0
check = 0
for fruits in fields:
    for _ in range(10):
        start = wide_random() % 200001
        k = wide_random() % 200001
        got = max_total_fruits(fruits, start, k)
        total += got
        check = (check * 31 + got) % 1000000007
print(f"200 walks: {total} fruits, checksum {check}")
