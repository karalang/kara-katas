# LeetCode #866: Prime Palindrome -- Python mirror of the bench program
# (the ★ arm, the odd-length palindromes in order).


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


def prime_palindrome(n):
    if 8 <= n <= 11:
        return 11
    root = 1
    while True:
        y = odd_palindrome(root)
        if y >= n and is_prime(y):
            return y
        root += 1


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


def main():
    queries = 60000
    total = 0
    check = 0
    for _ in range(queries):
        n = random_n()
        p = prime_palindrome(n)
        total += p
        check = (check * 31 + p) % 1000000007
    print(f"{queries} random n of 1 to 8 digits: answers sum to {total}, checksum {check}")


main()
