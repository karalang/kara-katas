# LeetCode #600: Non-negative Integers without Consecutive Ones -- walk
# the bits with Fibonacci counts.
#
# Mirrors find_integers.kara: at each one bit of n, from the top, the
# numbers with a 0 there and anything free below; two ones together in n
# end the walk.


def find_integers(n):
    fib = [1, 2]
    for k in range(2, 32):
        fib.append(fib[k - 1] + fib[k - 2])
    count = 0
    previous = False
    for k in range(31, -1, -1):
        if (n >> k) & 1 == 1:
            count += fib[k]
            if previous:
                return count
            previous = True
        else:
            previous = False
    return count + 1


# ---- test harness ---------------------------------------------------------

def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(n):
    print(f"n = {n} -> {find_integers(n)}")


def main():
    show(5)
    show(1)
    show(2)
    show(3)
    show(4)
    show(699050)
    show(1073741823)
    show(1000000000)
    small = [find_integers(n) for n in range(1, 41)]
    print(f"n = 1 to 40 -> {small}")
    seed = [600]
    total = 0
    checksum = 0
    for _ in range(300):
        hi = step(seed)
        lo = step(seed)
        n = 1 + (hi * 32768 + lo) % 1000000
        got = find_integers(n)
        total += got
        checksum = (checksum * 31 + got) % 1000000007
    print(f"300 random n up to 1000000: total {total}, checksum {checksum}")


main()
