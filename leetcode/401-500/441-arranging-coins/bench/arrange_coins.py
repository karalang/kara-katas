# Benchmark for #441: mirror of arrange_coins.kara (the closed form with
# an integer square root) on 3,000,000 random n up to 2^31 - 1.


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


seed = 441


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    count = 3000000
    total = 0
    checksum = 0
    for _ in range(count):
        high = next_random() * 32768 + next_random()
        n = 1 + (high * 2 + next_random() % 2) % 2147483647
        rows = arrange_coins(n)
        total += rows
        checksum = (checksum * 31 + rows) % 1000000007
    print(f"{count} random n: total {total}, checksum {checksum}")


main()
