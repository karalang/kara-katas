# LeetCode #441: Arranging Coins -- mirror of arrange_coins.kara (the
# closed form with an integer square root).


# The largest r with r * r <= x.
def isqrt(x):
    if x < 2:
        return x
    r = x
    nxt = (r + x // r) // 2
    while nxt < r:
        r = nxt
        nxt = (r + x // r) // 2
    return r


def arrange_coins(n):
    return (isqrt(8 * n + 1) - 1) // 2


def show(n):
    print(f"n = {n}: {arrange_coins(n)}")


seed = 441


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show(5)
    show(8)
    show(1)
    show(3)
    show(2147483647)
    show(2147450880)
    show(2147450879)
    show(1000000000)
    # 300 random n of at most 1 to 10 digits; a draw is below 2^30.
    total = 0
    checksum = 0
    for _ in range(300):
        digits = 1 + next_random() % 10
        top = 10 ** digits
        draw = next_random() * 32768 + next_random()
        n = 1 + draw % min(top, 2147483647)
        rows = arrange_coins(n)
        total += rows
        checksum = (checksum * 31 + rows) % 1000000007
    print(f"300 random n: total {total}, checksum {checksum}")


main()
