# LeetCode #842: Split Array into Fibonacci Sequence -- Python mirror of the ★ arm and its harness.

LIMIT = 2147483647


def read(d, start, length):
    if length > 1 and d[start] == 48:
        return -1
    value = 0
    for k in range(start, start + length):
        value = value * 10 + (d[k] - 48)
    return -1 if value > LIMIT else value


def split_into_fibonacci(num):
    d = num.encode()
    n = len(d)
    for i in range(1, 11):
        for j in range(1, 11):
            if i + j >= n:
                break
            a = read(d, 0, i)
            b = read(d, i, j)
            if a < 0 or b < 0:
                continue
            seq = [a, b]
            pos = i + j
            while pos < n:
                c = seq[-1] + seq[-2]
                if c > LIMIT:
                    break
                digits = str(c).encode()
                if pos + len(digits) > n:
                    break
                if d[pos:pos + len(digits)] != digits:
                    break
                seq.append(c)
                pos += len(digits)
            if pos == n:
                return seq
    return []


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(a, b, limit, spoil):
    s = f"{a}{b}"
    x, y = a, b
    while True:
        z = x + y
        w = str(z)
        if z > LIMIT or len(s) + len(w) > limit:
            break
        s += w
        x, y = y, z
    if next_random() % spoil == 0:
        cs = list(s)
        at = next_random() % len(cs)
        cs[at] = chr(48 + next_random() % 10)
        s = "".join(cs)
    return s


def show(num):
    print(f"\"{num}\" -> {split_into_fibonacci(num)}")


def main():
    global seed
    for s in ["1101111", "112358130", "0123", "123456579", "11235813", "000", "0000", "101", "1", "10",
              "1011", "214748364721474836422147483641", "2147483647021474836472147483647", "1023"]:
        show(s)
    seed = 842
    long = random_string(1, 1, 200, 1000000)
    print(f"{len(long)} digits from 1, 1: {len(split_into_fibonacci(long))} numbers")
    long = random_string(0, 0, 200, 1000000)
    print(f"{len(long)} digits from 0, 0: {len(split_into_fibonacci(long))} numbers")
    long = random_string(98765, 43210, 200, 1000000)
    print(f"{len(long)} digits from 98765, 43210: {split_into_fibonacci(long)}")
    found = 0
    check = 0
    for _ in range(300):
        a = next_random() % [10, 1000, 100000][next_random() % 3]
        b = next_random() % [10, 1000, 100000][next_random() % 3]
        limit = 3 + next_random() % 60
        s = random_string(a, b, limit, 3)
        seq = split_into_fibonacci(s)
        if seq:
            found += 1
        for x in seq:
            check = (check * 31 + x) % 1000000007
        check = (check * 31 + len(seq)) % 1000000007
    print(f"300 random strings: {found} split, checksum {check}")


main()
