# LeetCode #1300: Sum of Mutated Array Closest to Target -- Python mirror of
# the ★ arm (the numbers sorted and walked from the smallest; the best cap is
# the target's share of what is left, rounded down or up).


def find_best_value(arr, target):
    s = sorted(arr)
    n = len(s)
    before = 0
    for i in range(n):
        left = n - i
        if before + s[i] * left >= target:
            x = (target - before) // left
            low = abs(before + x * left - target)
            high = abs(before + (x + 1) * left - target)
            return x if low <= high else x + 1
        before += s[i]
    return s[n - 1]


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def wide():
    hi = next_random()
    return hi * 32768 + next_random()


def main():
    global seed
    print(f"{find_best_value([4, 9, 3], 10)} {find_best_value([2, 3, 5], 10)} {find_best_value([60864, 25176, 27249, 21296, 20204], 56803)} {find_best_value([1, 2, 3], 100)} {find_best_value([5, 5], 1)} {find_best_value([1, 10, 10], 13)}")
    seed = 1300
    total = 0
    check = 0
    for i in range(900):
        n = 1 + next_random() % 200
        top = 10 if i % 3 == 0 else 1000 if i % 3 == 1 else 100000
        arr = []
        s = 0
        for _ in range(n):
            x = 1 + wide() % top
            arr.append(x)
            s += x
        cap = s if s < 100000 else 100000
        if i % 3 == 2:
            target = 1 + wide() % 100000
        else:
            target = 1 + wide() % cap
        best = find_best_value(arr, target)
        total += best
        check = (check * 131 + best) % 1000000007
    print(f"900 random arrays: values total {total}, checksum {check}")


main()
