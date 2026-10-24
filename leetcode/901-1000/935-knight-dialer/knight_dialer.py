# LeetCode #935: Knight Dialer -- counts by last digit, one jump at a time
# (Python mirror).

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


# ---- test harness ---------------------------------------------------------


def main():
    print(f"n = 1: {knight_dialer(1)}")
    print(f"n = 2: {knight_dialer(2)}")
    print(f"n = 3131: {knight_dialer(3131)}")
    print("n from 1 to 10: " + ", ".join(str(knight_dialer(n)) for n in range(1, 11)))
    print(f"n = 23: {knight_dialer(23)}, n = 24: {knight_dialer(24)}")
    total = 0
    check = 0
    for n in range(1, 301):
        a = knight_dialer(n)
        total += a
        check = (check * 1000003 + a) % 1000000007
    print(f"n from 1 to 300: answers summing to {total}, checksum {check}")
    print(f"n = 4999: {knight_dialer(4999)}, n = 5000: {knight_dialer(5000)}, n = 2048: {knight_dialer(2048)}")


main()
