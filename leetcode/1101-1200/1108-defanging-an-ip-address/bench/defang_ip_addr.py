# LeetCode #1108: Defanging an IP Address -- the bench in Python: the ★
# arm (one pass, each period written as `[.]`) over 1024 random addresses,
# each round replacing one address with a new one and defanging every
# address again.


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
    a = next_random() % 256
    b = next_random() % 256
    c = next_random() % 256
    d = next_random() % 256
    return f"{a}.{b}.{c}.{d}"


def main():
    addresses = [random_address() for _ in range(1024)]
    length = 0
    check = 0
    calls = 0
    for rnd in range(10000):
        addresses[(rnd * 7919) % 1024] = random_address()
        for a in addresses:
            d = defang_ip_addr(a)
            length += len(d)
            if calls % 64 == 0:
                for c in d:
                    check = (check * 31 + ord(c)) % 1000000007
            calls += 1
    print(f"10000 rounds over 1024 addresses: {calls} calls, {length} characters, checksum {check}")


main()
