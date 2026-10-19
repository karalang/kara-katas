# LeetCode 793 -- Preimage Size of Factorial Zeroes Function, binary
# search. Python mirror of the ★ arm and its harness.


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


def show(k):
    print(f"k = {k} -> {preimage_size_fzf(k)}")


def main():
    for k in [0, 5, 3, 6, 11, 29, 30, 1000000000]:
        show(k)
    fives = 0
    check = 0
    for _ in range(300):
        a = next_random()
        b = next_random()
        k = (a * 32768 + b) % 1000000001
        answer = preimage_size_fzf(k)
        if answer == 5:
            fives += 1
        check = (check * 131 + k % 1000 + answer) % 1000000007
    print(f"300 random k: {fives} with five, checksum {check}")


main()
