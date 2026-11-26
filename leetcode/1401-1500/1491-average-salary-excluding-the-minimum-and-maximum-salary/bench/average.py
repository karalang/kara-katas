# LeetCode #1491: Average Salary Excluding the Minimum and Maximum Salary --
# the bench in Python, mirroring average.kara: one pass keeping the sum, the
# least and the most.
import math


def average(salary):
    least = most = salary[0]
    total = 0
    for s in salary:
        if s < least:
            least = s
        if s > most:
            most = s
        total += s
    return (total - least - most) / (len(salary) - 2)


def main():
    salary = [1000 + 9000 * k for k in range(100)]
    check = 0
    for p in range(2000000):
        k = p % 100
        salary[k] = 1000 + 9000 * k + (check + p) % 9000
        # half away from zero, as Kāra's `round` is
        cents = math.floor(average(salary) * 100.0 + 0.5)
        check = (check * 31 + cents) % 1000000007
    print(f"2000000 calls: checksum {check}")


main()
