# Benchmark: LeetCode #949 Largest Time for Given Digits -- the ★ arm,
# every arrangement, on all 10000 arrays of four digits. Mirrors
# largest_time_from_digits.kara, .c, .rs and go-seq/.


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


def main():
    rounds, count = 500, 10000
    arrays = [[a // 1000, a // 100 % 10, a // 10 % 10, a % 10] for a in range(count)]
    times = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            s = largest_time_from_digits(arrays[(r * 37 + i) % count])
            v = 0
            for c in s.encode():
                v = v * 131 + c
            if len(s) > 0:
                times += 1
            check = (check * 1000003 + v) % 1000000007
    print(f"{rounds} rounds over all {count} arrays of four digits: {times} times, checksum {check}")


main()
