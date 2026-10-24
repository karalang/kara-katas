# LeetCode #949: Largest Time for Given Digits -- every arrangement.
# Mirrors largest_time_from_digits.kara (the ★ arm) and its harness.


def largest_time_from_digits(arr):
    best = -1
    for i in range(4):
        for j in range(4):
            if j == i:
                continue
            for k in range(4):
                if k == i or k == j:
                    continue
                l = 6 - i - j - k
                hours = arr[i] * 10 + arr[j]
                minutes = arr[k] * 10 + arr[l]
                if hours < 24 and minutes < 60:
                    best = max(best, hours * 60 + minutes)
    if best < 0:
        return ""
    return f"{best // 600}{best // 60 % 10}:{best % 60 // 10}{best % 10}"


def show(arr):
    return f"[{arr[0]},{arr[1]},{arr[2]},{arr[3]}]"


def main():
    examples = [
        [1, 2, 3, 4],
        [5, 5, 5, 5],
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [2, 0, 6, 6],
        [1, 9, 6, 0],
        [9, 5, 3, 2],
        [2, 4, 5, 9],
    ]
    for arr in examples:
        print(f'{show(arr)}: "{largest_time_from_digits(arr)}"')
    times = 0
    minutes = 0
    check = 0
    seen = [0] * 1440
    for code in range(10000):
        arr = [code // 1000, code // 100 % 10, code // 10 % 10, code % 10]
        s = largest_time_from_digits(arr)
        m = -1
        if len(s) > 0:
            h = int(s[0:2])
            m = h * 60 + int(s[3:5])
            times += 1
            minutes += m
            seen[m] += 1
        check = (check * 31 + m + 1) % 1000000007
    print(f"all 10000 arrays of four digits: {times} make a time, minutes adding to {minutes}, checksum {check}")
    distinct = 0
    common = 0
    for t in range(1440):
        if seen[t] > 0:
            distinct += 1
        if seen[t] > seen[common]:
            common = t
    print(f"{distinct} different times; the most common, {common // 600}{common // 60 % 10}:{common % 60 // 10}{common % 10}, from {seen[common]} arrays")


main()
