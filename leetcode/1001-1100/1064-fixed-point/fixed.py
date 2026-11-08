# LeetCode #1064: Fixed Point -- the Python mirror of fixed.kara (the ★
# arm): `arr[i] - i` never falls, so a binary search finds the first index
# where it is not below 0, and that index is the answer if it is 0 there.


def fixed_point(arr):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if arr[mid] < mid:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo < len(arr) and arr[lo] == lo else -1


seed = 1064


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_sorted(n, start, gap):
    x = next_random() % (2 * start + 1) - start
    arr = []
    for _ in range(n):
        arr.append(x)
        x += 1 + next_random() % gap
    return arr


def show(arr):
    return "[" + ", ".join(str(x) for x in arr) + "]"


def main():
    examples = [[-10, -5, 0, 3, 7], [0, 2, 5, 8, 17], [-10, -5, 3, 4, 7, 9], [0], [5], [-1, 1], [-3, -2, 2, 3], [1, 2, 3, 4], [-1000000000, 1, 1000000000], [-5, -3, -1, 1, 3, 5]]
    for arr in examples:
        print(f"{show(arr)} -> {fixed_point(arr)}")
    total = check = 0
    for _ in range(3000):
        n = next_random() % 12 + 1
        start = next_random() % 6
        gap = next_random() % 3 + 1
        answer = fixed_point(random_sorted(n, start, gap))
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"3000 arrays of 1 to 12 numbers: sum {total}, checksum {check}")
    total = check = 0
    for _ in range(300):
        n = next_random() % 251 + 50
        start = next_random() % 200
        gap = next_random() % 4 + 1
        answer = fixed_point(random_sorted(n, start, gap))
        total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"300 arrays of 50 to 300 numbers: sum {total}, checksum {check}")
    print(f"10000 own: {fixed_point(list(range(10000)))}")
    print(f"10000 one past: {fixed_point([i + 1 for i in range(10000)])}")
    print(f"10000 meeting at the end: {fixed_point([2 * i - 9999 for i in range(10000)])}")
    print(f"10000 far apart: {fixed_point([i * 200000 - 999999999 for i in range(10000)])}")
    print(f"10000 random: {fixed_point(random_sorted(10000, 5000, 2))}")


main()
