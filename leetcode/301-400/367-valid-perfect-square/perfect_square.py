# LeetCode #367: Valid Perfect Square -- mirror of perfect_square.kara.


def is_perfect_square(num):
    lo, hi = 1, num
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        sq = mid * mid
        if sq == num:
            return True
        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1
    return False


def show(label, num):
    print(f"{label}: {'true' if is_perfect_square(num) else 'false'}")


def main():
    show("example 1", 16)
    show("example 2", 14)
    show("one", 1)
    show("two", 2)
    show("one below a square", 808200)
    show("a square", 808201)
    show("one above a square", 808202)
    show("a million", 1000000)
    show("the largest square in range", 2147395600)
    show("one above it", 2147395601)
    show("the largest input", 2147483647)
    seed = 367
    yes = 0
    checksum = 0
    for i in range(1000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        r = 1 + (seed // 65536) % 1000
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        num = r * r if i % 2 == 0 else 1 + (high * 32768 + seed // 65536) % 1000000
        ok = is_perfect_square(num)
        yes += ok
        checksum = (checksum * 2 + (1 if ok else 0)) % 1000000007
    print(f"1000 random numbers: {yes} squares, checksum {checksum}")


main()
