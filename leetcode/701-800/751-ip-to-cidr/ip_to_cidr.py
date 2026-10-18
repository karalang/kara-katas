# LeetCode 751 — IP to CIDR, greedy by the lowest set bit.
# Mirror of ip_to_cidr.kara (the ★ arm); same output, byte for byte.


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


class Rng:
    def __init__(self, seed):
        self.seed = seed

    def next(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed // 65536


def show(ip, n):
    print(f"{ip}, {n} -> [{', '.join(ip_to_cidr(ip, n))}]")


def main():
    for ip, n in [("255.0.0.7", 10), ("117.145.102.62", 8), ("0.0.0.0", 1),
                  ("0.0.0.0", 1000), ("255.255.255.255", 1), ("255.255.252.24", 1000),
                  ("1.2.3.4", 256), ("10.0.0.0", 256), ("192.168.1.1", 1),
                  ("192.168.1.255", 2)]:
        show(ip, n)
    rng = Rng(751)
    blocks = 0
    check = 0
    for _ in range(300):
        a = rng.next() % 255
        b = rng.next() % 256
        c = rng.next() % 256
        d = rng.next() % 256
        n = 1 + rng.next() % 1000
        for block in ip_to_cidr(f"{a}.{b}.{c}.{d}", n):
            blocks += 1
            for ch in block.encode():
                check = (check * 31 + ch) % 1000000007
    print(f"300 random ranges: {blocks} blocks in all, checksum {check}")


main()
