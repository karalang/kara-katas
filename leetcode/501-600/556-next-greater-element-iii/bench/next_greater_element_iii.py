# Benchmark for #556: Python mirror of the ★ arm (the next permutation of
# the digits); see next_greater_element_iii.kara.

seed = 556


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def next_greater_element(n):
    d = []
    x = n
    while x > 0:
        d.append(x % 10)
        x //= 10
    d.reverse()
    i = len(d) - 2
    while i >= 0 and d[i] >= d[i + 1]:
        i -= 1
    if i < 0:
        return -1
    j = len(d) - 1
    while d[j] <= d[i]:
        j -= 1
    d[i], d[j] = d[j], d[i]
    d[i + 1:] = reversed(d[i + 1:])
    out = 0
    for v in d:
        out = out * 10 + v
    return -1 if out > 2147483647 else out


def main():
    count = 500000
    numbers = []
    for t in range(count):
        top = 1000 if t % 3 == 0 else 10000000 if t % 3 == 1 else 2147483647
        a = next_random()
        b = next_random()
        numbers.append(1 + (a * 65536 + b) % top)
    found = 0
    checksum = 0
    for rnd in range(20):
        for g in range(count):
            got = next_greater_element(numbers[(rnd * 7 + g) % count])
            if got > 0:
                found += 1
            checksum = (checksum * 31 + got + 1) % 1000000007
    print(f"{count} numbers, 20 rounds each: {found} have a next, checksum {checksum}")


main()
