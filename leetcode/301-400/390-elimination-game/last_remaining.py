# LeetCode #390: Elimination Game -- Python mirror of last_remaining.kara.


def last_remaining(n):
    head, step, left, from_left = 1, 1, n, True
    while left > 1:
        if from_left or left % 2 == 1:
            head += step
        left //= 2
        step *= 2
        from_left = not from_left
    return head


def main():
    print(f"n = 9: {last_remaining(9)}")
    print(f"n = 1: {last_remaining(1)}")
    print("n = 1 to 24:" + "".join(f" {last_remaining(n)}" for n in range(1, 25)))
    for n in [2, 3, 4, 8, 16, 1024, 65536, 99999, 100000]:
        print(f"n = {n}: {last_remaining(n)}")
    total = 0
    checksum = 0
    for n in range(1, 2001):
        r = last_remaining(n)
        total += r
        checksum = (checksum * 31 + r) % 1000000007
    print(f"n = 1 to 2000: sum {total}, checksum {checksum}")


main()
