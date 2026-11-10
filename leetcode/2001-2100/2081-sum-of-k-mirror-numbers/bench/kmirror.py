# LeetCode #2081: Sum of k-Mirror Numbers -- Python mirror of the ★ arm's
# benchmark (kmirror.kara): every base from 2 to 9 asked for every n from
# 1 to 32, each search started afresh: 256 searches.


def is_mirror(x, k):
    digits = []
    while x > 0:
        digits.append(x % k)
        x //= k
    m = len(digits)
    for i in range(m // 2):
        if digits[i] != digits[m - 1 - i]:
            return False
    return True


def k_mirror(k, n):
    total = 0
    found = 0
    length = 1
    while True:
        half = (length + 1) // 2
        start = 10 ** (half - 1)
        for h in range(start, start * 10):
            p = h
            rest = h // 10 if length % 2 == 1 else h
            while rest > 0:
                p = p * 10 + rest % 10
                rest //= 10
            if is_mirror(p, k):
                total += p
                found += 1
                if found == n:
                    return total
        length += 1


def main():
    total = 0
    check = 0
    for k in range(2, 10):
        for n in range(1, 33):
            a = k_mirror(k, n)
            total += a
            check = (check * 31 + a) % 1000000007
    print(f"256 answers: sum {total}, checksum {check}")


main()
