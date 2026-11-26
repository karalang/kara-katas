# LeetCode #1491: Average Salary Excluding the Minimum and Maximum Salary --
# the Python mirror of the ★ arm: one pass keeping the sum, the least and
# the most.
import math


def average(salary):
    least = most = salary[0]
    total = 0
    for s in salary:
        least = min(least, s)
        most = max(most, s)
        total += s
    return (total - least - most) / (len(salary) - 2)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def salaries(n):
    s = []
    nxt = 1000 + next_random() % 1000
    for _ in range(n):
        s.append(nxt)
        nxt += 1 + next_random() % (990000 // n)
    for i in range(n - 1, 0, -1):
        j = next_random() % (i + 1)
        s[i], s[j] = s[j], s[i]
    return s


def main():
    global seed
    print(f"{average([4000, 3000, 1000, 2000]):.5f}")
    print(f"{average([1000, 2000, 3000]):.5f}")
    print(f"{average([1000, 1000000, 500000]):.5f}")
    print(f"{average([1001, 1002, 1000]):.5f}")
    print(f"{average([1000000, 5000, 7000, 6000, 1000]):.5f}")
    print(f"{average([1000, 2000, 2001, 2003, 9000]):.5f}")
    seed = 1491
    big = salaries(100)
    print(f"100 salaries: {average(big):.5f}")
    check = 0
    for _ in range(3000):
        n = 3 + next_random() % 98
        s = salaries(n)
        # half away from zero, as Kāra's `round` is
        cents = math.floor(average(s) * 100.0 + 0.5)
        check = (check * 31 + cents) % 1000000007
    print(f"3000 random lists: checksum {check}")


main()
