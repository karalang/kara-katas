# LeetCode #2243: Calculate Digit Sum of a String -- the benchmark's
# Python mirror of digits.kara: while the string is longer than k, it is
# rebuilt group by group, each group's digits summed and the sum written
# back.


def digit_sum(s, k):
    current = s
    while len(current) > k:
        next_ = ""
        start = 0
        while start < len(current):
            end = min(start + k, len(current))
            total = 0
            for ch in current[start:end]:
                total += ord(ch) - ord("0")
            next_ += f"{total}"
            start = end
        current = next_
    return current


seed = 2243


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digits_of():
    return "".join(str(next_random() % 10) for _ in range(100))


def main():
    strings = [digits_of() for _ in range(1000)]
    check = 0
    for p in range(200):
        at = next_random() % 1000
        strings[at] = digits_of()
        k = p % 4 + 2
        for s in strings:
            for ch in digit_sum(s, k):
                check = (check * 31 + ord(ch)) % 1000000007
    print(f"200 passes over 1000 strings: checksum {check}")


main()
