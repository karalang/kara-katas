# LeetCode #1646: Get Maximum in Generated Array -- the Python mirror of
# the ★ arm: the array built by its two rules, the largest kept.


def get_maximum_generated(n):
    if n == 0:
        return 0
    nums = [0] * (n + 1)
    nums[1] = 1
    best = 1
    for i in range(2, n + 1):
        nums[i] = nums[i // 2] if i % 2 == 0 else nums[i // 2] + nums[i // 2 + 1]
        best = max(best, nums[i])
    return best


# ---- the harness: the same as every arm's ---------------------------------

seed = 1646


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def batch(count, most):
    check = 0
    total = 0
    for _ in range(count):
        n = next_random() % (most + 1)
        found = get_maximum_generated(n)
        total += found
        check = (check * 31 + found + 1) % 1000000007
    print(f"{count} random n up to {most}: maxima sum to {total}, checksum {check}")


print(get_maximum_generated(7))
print(get_maximum_generated(2))
print(get_maximum_generated(3))
print(get_maximum_generated(0))
print(get_maximum_generated(1))
print(get_maximum_generated(100))
print(" ".join(str(get_maximum_generated(n)) for n in range(101)))
batch(3000, 100)
