# Benchmark for #670: the last place of each digit, as the Kara ★ arm.


def digits_of(num):
    d = []
    x = num
    while x > 0:
        d.append(x % 10)
        x //= 10
    if not d:
        d.append(0)
    d.reverse()
    return d


def number_of(d):
    x = 0
    for v in d:
        x = x * 10 + v
    return x


def maximum_swap(num):
    d = digits_of(num)
    last = [-1] * 10
    for i in range(len(d)):
        last[d[i]] = i
    for i in range(len(d)):
        v = 9
        while v > d[i]:
            if last[v] > i:
                j = last[v]
                d[j] = d[i]
                d[i] = v
                return number_of(d)
            v -= 1
    return num


def main():
    count = 3000000
    s = 0
    for i in range(count):
        s = (s * 31 + maximum_swap(i * 33 + i % 7)) % 1000000007
    print(f"{count} numbers: checksum {s}")


main()
