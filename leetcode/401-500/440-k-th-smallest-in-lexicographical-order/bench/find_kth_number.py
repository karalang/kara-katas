# Benchmark for #440: mirror of find_kth_number.kara (counting down the
# denary tree) on 1,000,000 random queries with n up to 10^9.


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


seed = 440


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = 1000000
    total = 0
    checksum = 0
    for _ in range(queries):
        n = 1 + (next_random() * 32768 + next_random()) % 1000000000
        k = 1 + (next_random() * 32768 + next_random()) % n
        x = find_kth_number(n, k)
        total += x
        checksum = (checksum * 31 + x) % 1000000007
    print(f"{queries} queries with n up to 10^9: total {total}, checksum {checksum}")


main()
