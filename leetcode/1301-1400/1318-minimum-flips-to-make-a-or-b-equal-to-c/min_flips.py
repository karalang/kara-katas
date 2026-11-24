# LeetCode #1318: Minimum Flips to Make a OR b Equal to c -- Python mirror
# of the ★ Kāra arm: each of the 30 bits a number up to 10^9 can have
# looked at alone; where c wants a 1 it costs one flip if a and b are both
# 0, and where c wants a 0 it costs one flip for each of a and b that has
# a 1.


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
    print(f"{min_flips(2, 6, 5)} {min_flips(4, 2, 7)} {min_flips(1, 2, 3)} {min_flips(big, 999999999, 1)} {min_flips(1, 1, big)} {min_flips(big, big, big)}")
    seed = 1318

    def nr():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    total = 0
    check = 0
    for t in range(100000):
        top = 15 if t % 2 == 0 else big
        hi = nr(); a = 1 + (hi * 32768 + nr()) % top
        hi = nr(); b = 1 + (hi * 32768 + nr()) % top
        hi = nr(); c = 1 + (hi * 32768 + nr()) % top
        got = min_flips(a, b, c)
        total += got
        check = (check * 31 + got) % 1000000007
    print(f"100000 random triples: flips total {total}, checksum {check}")


main()
