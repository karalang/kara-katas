# LeetCode 793 -- Preimage Size of Factorial Zeroes Function: the bench,
# in Python. Mirrors preimage_size_fzf.kara: binary search for the least
# x whose factorial has at least k zeroes at the end.


def zeroes(x):
    count = 0
    p = x // 5
    while p > 0:
        count += p
        p //= 5
    return count


def preimage_size_fzf(k):
    lo, hi = 0, 5 * k + 5
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if zeroes(mid) < k:
            lo = mid + 1
        else:
            hi = mid
    return 5 if zeroes(lo) == k else 0


seed = 793


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 4000000
    fives = 0
    check = 0
    for _ in range(rounds):
        a = next_random()
        b = next_random()
        k = (a * 32768 + b) % 1000000001
        answer = preimage_size_fzf(k)
        if answer == 5:
            fives += 1
        check = (check * 131 + k % 1000 + answer) % 1000000007
    print(f"{rounds} values of k: {fives} with five, checksum {check}")


main()
