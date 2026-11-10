# LeetCode #1108: Defanging an IP Address -- the Python mirror of the ★
# arm: one pass over the characters, each period written as `[.]`.


def defang_ip_addr(address):
    out = []
    for c in address:
        if c == '.':
            out.append("[.]")
        else:
            out.append(c)
    return "".join(out)


seed = 1108


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_address():
    parts = []
    for _ in range(4):
        k = next_random() % 3
        if k == 0:
            n = next_random() % 10
        elif k == 1:
            n = next_random() % 100
        else:
            n = next_random() % 256
        parts.append(str(n))
    return ".".join(parts)


def main():
    cases = ["1.1.1.1", "255.100.50.0", "0.0.0.0", "255.255.255.255", "10.0.0.1", "192.168.1.254", "8.8.4.4", "127.0.0.1", "1.22.133.4"]
    for a in cases:
        print(f"{a} -> {defang_ip_addr(a)}")
    length = 0
    check = 0
    for _ in range(2000):
        d = defang_ip_addr(random_address())
        length += len(d)
        for c in d:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"2000 random addresses: {length} characters, checksum {check}")


main()
