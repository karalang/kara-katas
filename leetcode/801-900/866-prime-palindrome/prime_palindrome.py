# LeetCode #866: Prime Palindrome -- Python mirror of the ★ arm (the
# odd-length palindromes in order).


def prime_palindrome(n):
    if 8 <= n <= 11:
        return 11
    root = 1
    while True:
        y = odd_palindrome(root)
        if y >= n and is_prime(y):
            return y
        root += 1


def odd_palindrome(root):
    y = root
    rest = root // 10
    while rest > 0:
        y = y * 10 + rest % 10
        rest //= 10
    return y


def is_prime(x):
    if x < 2:
        return False
    if x % 2 == 0:
        return x == 2
    d = 3
    while d * d <= x:
        if x % d == 0:
            return False
        d += 2
    return True


seed = 866


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_n():
    digits = 1 + next_random() % 8
    low = 10 ** (digits - 1)
    hi = next_random()
    lo = next_random()
    return low + (hi * 32768 + lo) % (9 * low)


def show(n):
    print(f"n = {n} -> {prime_palindrome(n)}")


def main():
    show(6)
    show(8)
    show(13)
    for n in [1, 2, 11, 12, 102, 9990, 1000000, 9989899, 9989900, 100000000]:
        show(n)
    total = 0
    check = 0
    for n in range(1, 2001):
        p = prime_palindrome(n)
        total += p
        check = (check * 31 + p) % 1000000007
    print(f"n from 1 to 2000: answers sum to {total}, checksum {check}")
    total = 0
    check = 0
    longer = 0
    for _ in range(200):
        n = random_n()
        p = prime_palindrome(n)
        total += p
        check = (check * 31 + p) % 1000000007
        if len(str(p)) > len(str(n)):
            longer += 1
    print(f"200 random n of 1 to 8 digits: {longer} answers longer than n, answers sum to {total}, checksum {check}")


main()
