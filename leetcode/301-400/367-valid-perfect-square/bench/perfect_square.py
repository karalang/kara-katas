# Benchmark for #367 -- mirror of perfect_square.kara.


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


def main():
    seed = 367
    yes = 0
    checksum = 0
    for i in range(3000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        high = seed // 65536
        seed = (seed * 1103515245 + 12345) % 2147483648
        wide = high * 32768 + seed // 65536
        if i % 2 == 0:
            r = 1 + wide % 46340
            num = r * r
        else:
            num = 1 + wide + (i // 2 % 2) * 1073741823
        if is_perfect_square(num):
            yes += 1
            checksum = (checksum * 31 + i) % 1000000007
    print(f"{yes} squares, checksum {checksum}")


main()
