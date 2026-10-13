# LeetCode #481: Magical String -- mirror of magical_string.kara (the ★ arm).


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    print(f"n = 6 -> {magical_string(6)}")
    print(f"n = 1 -> {magical_string(1)}")
    print("n = 1 to 20 -> " + ", ".join(str(magical_string(n)) for n in range(1, 21)))
    digits = []
    before = 0
    for n in range(1, 61):
        now = magical_string(n)
        digits.append("1" if now > before else "2")
        before = now
    print(f"first 60 digits from the counts: {''.join(digits)}")
    print(f"n = 99999 -> {magical_string(99999)}")
    print(f"n = 100000 -> {magical_string(100000)}")
    count = 300
    seed = [481]
    total = 0
    checksum = 0
    for c in range(count):
        n = 1 + next_random(seed) % 3000
        if c % 50 == 49:
            n = 1 + (next_random(seed) * 32768 + next_random(seed)) % 100000
        ones = magical_string(n)
        total += ones
        checksum = (checksum * 31 + ones * 7 + n) % 1000000007
    print(f"{count} random cases: 1s add up to {total}, checksum {checksum}")


main()
