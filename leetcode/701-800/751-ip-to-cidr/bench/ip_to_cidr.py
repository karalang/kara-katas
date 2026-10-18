# LeetCode 751 — IP to CIDR, bench: the ★ arm (greedy by the lowest
# set bit) on half a million ranges from a pool of 1000 addresses.
# Mirrors ip_to_cidr.kara.


def address(ip):
    x = 0
    for part in ip.split('.'):
        x = x * 256 + int(part)
    return x


def dotted(x):
    return f"{x // 16777216 % 256}.{x // 65536 % 256}.{x // 256 % 256}.{x % 256}"


def ip_to_cidr(ip, n):
    x = address(ip)
    left = n
    out = []
    while left > 0:
        size = 4294967296 if x == 0 else x & -x
        while size > left:
            size //= 2
        bits = 0
        while (1 << bits) < size:
            bits += 1
        out.append(f"{dotted(x)}/{32 - bits}")
        x += size
        left -= size
    return out


seed = 751


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    queries = 500000
    pool = []
    for _ in range(1000):
        a = next_random() % 255
        b = next_random() % 256
        c = next_random() % 256
        d = next_random() % 256
        pool.append(f"{a}.{b}.{c}.{d}")
    blocks = 0
    check = 0
    for q in range(queries):
        n = 1 + next_random() % 1000
        found = ip_to_cidr(pool[q % 1000], n)
        blocks += len(found)
        for block in found:
            check = (check * 31 + len(block)) % 1000000007
    print(f"{queries} ranges: {blocks} blocks in all, checksum {check}")


main()
