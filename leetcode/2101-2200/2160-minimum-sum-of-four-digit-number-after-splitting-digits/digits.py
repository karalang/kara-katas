# LeetCode #2160: Minimum Sum of Four Digit Number After Splitting Digits
# -- the Python mirror of digits.kara, the ★ arm: the digits sorted, the
# two smallest to the tens and the two largest to the ones.


def minimum_sum(num):
    d = sorted(int(c) for c in str(num))
    return (d[0] * 10 + d[2]) + (d[1] * 10 + d[3])


seed = 2160


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(num):
    print(f"{num} -> {minimum_sum(num)}")


def main():
    show(2932)
    show(4009)
    show(1000)
    show(9999)
    show(1234)
    show(5050)
    total = 0
    check = 0
    for _ in range(2000):
        num = next_random() % 9000 + 1000
        s = minimum_sum(num)
        total += s
        check = (check * 31 + s + 1) % 1000000007
    print(f"2000 numbers: {total} in all, checksum {check}")
    every = 0
    h = 0
    for num in range(1000, 10000):
        s = minimum_sum(num)
        every += s
        h = (h * 31 + s + 1) % 1000000007
    print(f"all 9000: {every} in all, checksum {h}")


main()
