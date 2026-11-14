# LeetCode #1534: Count Good Triplets -- bench: the ★ arm over 100 random
# arrays of 100 values up to 1000, each with its own a, b and c up to
# 1000, built once and answered 10 times. Python mirror of triplets.kara.


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


cases = []
for _ in range(100):
    arr = [next_random() % 1001 for _ in range(100)]
    a = next_random() % 1001
    b = next_random() % 1001
    c = next_random() % 1001
    cases.append((arr, a, b, c))
check = 0
for _ in range(10):
    for arr, a, b, c in cases:
        check = mix(check, count_good_triplets(arr, a, b, c))
print(f"10 passes over 100 arrays of 100 values: checksum {check}")
