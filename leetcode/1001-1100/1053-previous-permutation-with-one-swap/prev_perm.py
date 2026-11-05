# LeetCode #1053: Previous Permutation With One Swap -- one scan from the
# right. The Python mirror of prev_perm.kara; its output is byte-identical.


def prev_perm_opt1(arr):
    out = list(arr)
    n = len(out)
    i = n - 2
    while i >= 0 and out[i] <= out[i + 1]:
        i -= 1
    if i < 0:
        return out
    j = n - 1
    while out[j] >= out[i]:
        j -= 1
    while out[j - 1] == out[j]:
        j -= 1
    out[i], out[j] = out[j], out[i]
    return out


# ---- test harness ----

class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def random_values(n, largest, rng):
    return [rng.next() % largest + 1 for _ in range(n)]


def fold(arr):
    h = 0
    for x in arr:
        h = (h * 10007 + x) % 1000000007
    return h


def main():
    examples = [
        [3, 2, 1],
        [1, 1, 5],
        [1, 9, 4, 6, 7],
        [3, 1, 1, 3],
        [7],
        [2, 1],
        [1, 2],
        [5, 5, 5],
        [4, 1, 2, 2, 3],
        [6, 2, 2, 5, 5, 1],
    ]
    for arr in examples:
        print(f"{arr} -> {prev_perm_opt1(arr)}")
    rng = Rng(1053)
    changed = 0
    check = 0
    for _ in range(3000):
        n = rng.next() % 8 + 1
        arr = random_values(n, 4, rng)
        answer = prev_perm_opt1(arr)
        if answer != arr:
            changed += 1
        check = (check * 131 + fold(answer)) % 1000000007
    print(f"3000 random arrays of 1 to 8 values of 1 to 4: {changed} changed, checksum {check}")
    changed = 0
    check = 0
    for _ in range(300):
        n = rng.next() % 2000 + 1
        arr = random_values(n, 10000, rng)
        answer = prev_perm_opt1(arr)
        if answer != arr:
            changed += 1
        check = (check * 131 + fold(answer)) % 1000000007
    print(f"300 random arrays of 1 to 2000 values of 1 to 10000: {changed} changed, checksum {check}")
    first_high = list(range(1, 10001))
    first_high[0] = 5000
    a = prev_perm_opt1(first_high)
    print(f"10000 rising, the first 5000 -> starts {a[0]}, {a[1]}, checksum {fold(a)}")
    last_two = list(range(1, 10001))
    last_two[9998], last_two[9999] = last_two[9999], last_two[9998]
    b = prev_perm_opt1(last_two)
    print(f"10000 rising, the last two swapped -> ends {b[9998]}, {b[9999]}, checksum {fold(b)}")


main()
