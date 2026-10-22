# Benchmark for #842: Split Array into Fibonacci Sequence -- Python twin of
# the Kāra ★ arm (the first two numbers decide the rest).


def read(d, start, length):
    if length > 1 and d[start] == "0":
        return -1
    value = 0
    for k in range(start, start + length):
        value = value * 10 + ord(d[k]) - 48
    return -1 if value > 2147483647 else value


def split_into_fibonacci(d):
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
                if c > 2147483647:
                    break
                digits = str(c)
                if pos + len(digits) > n:
                    break
                if d[pos:pos + len(digits)] != digits:
                    break
                seq.append(c)
                pos += len(digits)
            if pos == n:
                return seq
    return []


def main():
    count, rounds = 64, 240000
    seed = 842

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    cases = []
    for g in range(count):
        top = [10, 1000, 100000][g % 3]
        x = next_random() % top
        y = next_random() % top
        s = f"{x}{y}"
        while True:
            z = x + y
            w = str(z)
            if z > 2147483647 or len(s) + len(w) > 200:
                break
            s += w
            x, y = y, z
        if g % 4 == 3:
            d = list(s)
            at = next_random() % len(d)
            d[at] = chr(48 + (ord(d[at]) - 48 + 1) % 10)
            s = "".join(d)
        cases.append(s)
    split = 0
    checksum = 0
    for rnd in range(rounds):
        seq = split_into_fibonacci(cases[rnd % count])
        if seq:
            split += 1
            checksum = (checksum * 31 + len(seq) * 1000 + seq[-1] % 1000) % 1000000007
        else:
            checksum = (checksum * 31 + 7) % 1000000007
    print(f"{rounds} rounds of {count} strings: {split} split, checksum {checksum}")


main()
