# LeetCode #1015: Smallest Integer Divisible by K -- bench
# Mirrors repunit.kara; see ../README.md § Benchmarks.


def smallest_repunit_div_by_k(k):
    if k % 2 == 0 or k % 5 == 0:
        return -1
    r = 0
    for length in range(1, k + 1):
        r = (r * 10 + 1) % k
        if r == 0:
            return length
    return -1


def main():
    last = 30000
    none = 0
    total = 0
    check = 0
    for k in range(1, last + 1):
        answer = smallest_repunit_div_by_k(k)
        if answer < 0:
            none += 1
        else:
            total += answer
        check = (check * 31 + answer + 1) % 1000000007
    print(f"k = 1..{last}: {none} with no answer, the rest sum to {total}, checksum {check}")


main()
