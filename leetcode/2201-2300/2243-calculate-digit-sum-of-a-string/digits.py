# LeetCode #2243: Calculate Digit Sum of a String -- the Python mirror of
# digits.kara: while the string is longer than k, it is rebuilt group by
# group, each group of k characters (the last perhaps shorter) cut by a
# slice, its digits summed, and the sum written back.


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


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digits_of(length, top):
    return "".join(str(next_random() % top) for _ in range(length))


def main():
    global seed
    examples = [
        ("11111222223", 3),
        ("00000000", 3),
        ("1234", 4),
        ("9999", 2),
        ("98765", 2),
        ("9" * 100, 2),
    ]
    for s, k in examples:
        print(f"{s} {k} -> {digit_sum(s, k)}")
    seed = 2243
    check = 0
    length_total = 0
    for c in range(3000):
        length = next_random() % 100 + 1
        top = next_random() % 10 + 1
        s = digits_of(length, top)
        k = next_random() % 99 + 2 if c < 1500 else next_random() % 4 + 2
        answer = digit_sum(s, k)
        length_total += len(answer)
        for ch in answer:
            check = (check * 31 + ord(ch)) % 1000000007
    print(f"3000 strings: {length_total} digits answered, checksum {check}")


main()
