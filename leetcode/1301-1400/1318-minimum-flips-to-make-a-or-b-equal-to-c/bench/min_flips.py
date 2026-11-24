# LeetCode #1318 bench, Python mirror of the Kāra bench: the ★ arm (each of
# the 30 bits looked at alone and costed) on 1000 triples of numbers from 1
# to 10^9 built once; then 3000 passes, each setting one number of every
# triple from the checksum so far, and folding every answer plus the pass
# into the checksum.


def min_flips(a, b, c):
    flips = 0
    for i in range(30):
        x = (a >> i) & 1
        y = (b >> i) & 1
        z = (c >> i) & 1
        flips += 1 - (x | y) if z == 1 else x + y
    return flips


def main():
    big = 1000000000
    seed = 1318

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    nums = []
    for _ in range(3000):
        hi = nr()
        nums.append(1 + (hi * 32768 + nr()) % big)
    check = 0
    for p in range(3000):
        for t in range(1000):
            nums[3 * t + check % 3] = 1 + (check * 7919) % big
            got = min_flips(nums[3 * t], nums[3 * t + 1], nums[3 * t + 2])
            check = (check * 31 + got + p) % 1000000007
    print(f"3000 passes over 1000 triples: checksum {check}")


main()
