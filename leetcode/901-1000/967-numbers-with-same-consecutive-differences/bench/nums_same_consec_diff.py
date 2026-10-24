# Benchmark: LeetCode #967 Numbers With Same Consecutive Differences --
# the ★ arm, level by level, for every n from 2 to 9 and every k from 0
# to 9. Mirrors nums_same_consec_diff.kara, .c, .rs and go-seq/.


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


def main():
    rounds = 2000
    found = 0
    check = 0
    for _ in range(rounds):
        for n in range(2, 10):
            for k in range(10):
                for x in nums_same_consec_diff(n, k):
                    found += 1
                    check = (check * 31 + x) % 1000000007
    print(f"{rounds} rounds over n from 2 to 9 and k from 0 to 9: {found} numbers, checksum {check}")


main()
