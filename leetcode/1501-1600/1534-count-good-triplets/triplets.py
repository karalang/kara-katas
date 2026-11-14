# LeetCode #1534: Count Good Triplets -- Python mirror of triplets.kara
# (every i < j < k, the pair (i, j) checked first); output byte-identical.


def count_good_triplets(arr, a, b, c):
    n = len(arr)
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if abs(arr[i] - arr[j]) > a:
                continue
            for k in range(j + 1, n):
                if abs(arr[j] - arr[k]) <= b and abs(arr[i] - arr[k]) <= c:
                    count += 1
    return count


seed = 1534


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def batch(count, most, top):
    check = 0
    for _ in range(count):
        n = next_random() % (most - 2) + 3
        arr = [next_random() % (top + 1) for _ in range(n)]
        a = next_random() % (top + 1)
        b = next_random() % (top + 1)
        c = next_random() % (top + 1)
        check = mix(check, count_good_triplets(arr, a, b, c))
    print(f"{count} arrays of 3 to {most} values up to {top}: checksum {check}")


for arr, a, b, c in [([3, 0, 1, 1, 9, 7], 7, 2, 3), ([1, 1, 2, 2, 3], 0, 0, 1), ([0, 1000, 0], 1000, 1000, 0), ([5, 5, 5], 0, 0, 0)]:
    print(f"[{', '.join(map(str, arr))}], a = {a}, b = {b}, c = {c} -> {count_good_triplets(arr, a, b, c)}")
print(f"100 sevens, a = b = c = 0 -> {count_good_triplets([7] * 100, 0, 0, 0)}")
print(f"0 to 990 by 10, a = b = 10, c = 20 -> {count_good_triplets([i * 10 for i in range(100)], 10, 10, 20)}")
batch(3000, 12, 10)
batch(300, 100, 1000)
