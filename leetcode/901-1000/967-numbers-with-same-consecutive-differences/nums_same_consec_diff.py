# LeetCode #967: Numbers With Same Consecutive Differences -- level by
# level.
#
# Mirrors nums_same_consec_diff.kara: the numbers of one digit are 1 to
# 9; each number of the next length is one of these with a digit
# appended, its last digit plus or minus k where that is a digit (once
# when k is 0).


def nums_same_consec_diff(n, k):
    level = list(range(1, 10))
    for _ in range(1, n):
        nxt = []
        for x in level:
            last = x % 10
            if last + k <= 9:
                nxt.append(x * 10 + last + k)
            if k > 0 and last - k >= 0:
                nxt.append(x * 10 + last - k)
        level = nxt
    return level


# ---- test harness ---------------------------------------------------------


def show(v):
    return "[" + ",".join(str(x) for x in v) + "]"


def main():
    examples = [(3, 7), (2, 1), (2, 0), (2, 9), (3, 0), (3, 5), (4, 8), (2, 5)]
    for n, k in examples:
        got = sorted(nums_same_consec_diff(n, k))
        print(f"n = {n}, k = {k}: {show(got)}")
    total = 0
    all_sum = 0
    for n in range(2, 10):
        line = ""
        check = 0
        for k in range(10):
            got = sorted(nums_same_consec_diff(n, k))
            line += f" {len(got)}"
            total += len(got)
            for x in got:
                all_sum += x
                check = (check * 31 + x % 1000000007) % 1000000007
        print(f"n = {n}, k = 0 to 9:{line}, checksum {check}")
    print(f"{total} numbers in all, summing to {all_sum}")


main()
