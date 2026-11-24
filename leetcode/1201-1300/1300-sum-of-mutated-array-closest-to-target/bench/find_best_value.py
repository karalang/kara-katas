# LeetCode #1300 bench: the ★ arm (the numbers sorted and walked from the
# smallest; the best cap is the target's share of what is left, rounded down
# or up) over 50 arrays of 10^4 numbers, up to 20, 100, 1000, 10^4 or 10^5 in
# turn, built once; then 200 passes, each setting one number of every array
# and its target from the checksum so far, answering it, and folding the
# answer into the checksum.


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


seed = 1300


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    tops = [20, 100, 1000, 10000, 100000]
    arrays = []
    for t in range(50):
        arr = []
        for _ in range(10000):
            hi = next_random()
            arr.append(1 + (hi * 32768 + next_random()) % tops[t % 5])
        arrays.append(arr)
    check = 0
    for p in range(200):
        for t, arr in enumerate(arrays):
            arr[check % 10000] = 1 + check % tops[t % 5]
            target = 1 + (check * 7919) % 100000
            check = (check * 31 + find_best_value(arr, target) + p) % 1000000007
    print(f"200 passes over 50 arrays of 10^4: checksum {check}")


main()
