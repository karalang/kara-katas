# Benchmark for #481: Python mirror of the ★ arm (the string read while
# it is written); see magical_string.kara.


def magical_string(n):
    s = [1, 2, 2]
    read = 2
    while len(s) < n:
        nxt = 3 - s[-1]
        for _ in range(s[read]):
            s.append(nxt)
        read += 1
    ones = 0
    for i in range(n):
        if s[i] == 1:
            ones += 1
    return ones


def main():
    rounds = 1000
    total = 0
    checksum = 0
    for r in range(rounds):
        ones = magical_string(100000 - r)
        total += ones
        checksum = (checksum * 31 + ones) % 1000000007
    print(f"{rounds} rounds of n = 99001 to 100000: 1s add up to {total}, checksum {checksum}")


main()
