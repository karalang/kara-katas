# LeetCode #440: K-th Smallest in Lexicographical Order -- mirror of
# find_kth_number.kara (counting down the denary tree).


# The numbers in [1, n] that start with prefix.
def count_under(prefix, n):
    count = 0
    first = prefix
    last = prefix
    while first <= n:
        count += min(n, last) - first + 1
        first *= 10
        last = last * 10 + 9
    return count


def find_kth_number(n, k):
    current = 1
    left = k - 1
    while left > 0:
        under = count_under(current, n)
        if under <= left:
            left -= under
            current += 1
        else:
            left -= 1
            current *= 10
    return current


def show(n, k):
    print(f"n = {n}, k = {k}: {find_kth_number(n, k)}")


seed = 440


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(13, 2)
    show(1, 1)
    show(10, 3)
    show(100, 100)
    show(1000, 1000)
    show(10000, 5000)
    show(99999, 77777)
    show(100000, 1)
    # 300 random cases: n of 1 to 4 digits, k anywhere in [1, n].
    total = 0
    checksum = 0
    for _ in range(300):
        digits = 1 + next_random() % 4
        top = 10 ** digits
        n = 1 + next_random() % (top - 1)
        k = 1 + next_random() % n
        x = find_kth_number(n, k)
        total += x
        checksum = (checksum * 31 + x) % 1000000007
    print(f"300 random cases: total {total}, checksum {checksum}")


main()
