# LeetCode #1497: Check If Array Pairs Are Divisible by k -- the Python
# mirror of can_arrange.kara: each value's remainder by k counted.


def can_arrange(arr, k):
    count = [0] * k
    for x in arr:
        count[x % k] += 1
    if count[0] % 2 != 0:
        return False
    for r in range(1, k):
        if count[r] != count[k - r]:
            return False
    return True


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_values(n, k, spread):
    arr = []
    for i in range(n):
        x = next_random() % (2 * spread + 1) - spread
        if i % 2 == 1 and next_random() % 8 != 0:
            want = (k - arr[i - 1] % k) % k
            moved = x - x % k + want
            arr.append(moved - k if moved > spread else moved + k if moved < -spread else moved)
        else:
            arr.append(x)
    return arr


def b(x):
    return "true" if x else "false"


def main():
    global seed
    print(f"{b(can_arrange([1, 2, 3, 4, 5, 10, 6, 7, 8, 9], 5))} {b(can_arrange([1, 2, 3, 4, 5, 6], 7))} {b(can_arrange([1, 2, 3, 4, 5, 6], 10))}")
    edges = [([7, 3], 1), ([-1, -4], 5), ([-1, 6], 5), ([3, 3], 6), ([3, 0], 6), ([1000000000, -1000000000], 100000)]
    print(" ".join(b(can_arrange(a, k)) for a, k in edges))
    seed = 1497
    paired = []
    for _ in range(50000):
        x = next_random() * 30011 % 2000000001 - 1000000000
        paired.append(x)
        shift = 100000 * (next_random() % 5)
        paired.append(shift - x if x > 0 else -x - shift)
    moved = paired[:]
    moved[777] += 1
    mixed = random_values(100000, 99991, 1000000000)
    print(f"100000 values: {b(can_arrange(paired, 100000))} {b(can_arrange(moved, 100000))} {b(can_arrange(mixed, 99991))}")
    check = 0
    yes = 0
    for _ in range(3000):
        n = 2 * (1 + next_random() % 10)
        k = 1 + next_random() % 12
        arr = random_values(n, k, 50)
        can = can_arrange(arr, k)
        if can:
            yes += 1
        check = (check * 31 + (2 if can else 1)) % 1000000007
    print(f"3000 random arrays: {yes} pair, checksum {check}")


main()
