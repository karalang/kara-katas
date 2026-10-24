# LeetCode #935: Knight Dialer -- bench: counts by last digit, one jump
# at a time. Mirrors knight_dialer.kara, .c, .rs and go-seq/.

JUMPS = [[4, 6], [6, 8], [7, 9], [4, 8], [0, 3, 9], [], [0, 1, 7], [2, 6], [1, 3], [2, 4]]


def knight_dialer(n):
    modulus = 1000000007
    counts = [1] * 10
    for _ in range(1, n):
        nxt = [0] * 10
        for d in range(10):
            for frm in JUMPS[d]:
                nxt[d] = (nxt[d] + counts[frm]) % modulus
        counts = nxt
    total = 0
    for c in counts:
        total = (total + c) % modulus
    return total


def main():
    rounds = 20
    low = 4901
    high = 5000
    total = 0
    check = 0
    for r in range(rounds):
        # each round counts every length from low to high, starting from a
        # different one
        for i in range(high - low + 1):
            n = low + (r + i) % (high - low + 1)
            a = knight_dialer(n)
            total += a
            check = (check * 1000003 + a) % 1000000007
    print(f"{rounds} rounds over n from {low} to {high}: answers summing to {total}, checksum {check}")


main()
