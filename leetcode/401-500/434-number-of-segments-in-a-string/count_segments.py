# LeetCode #434: Number of Segments in a String -- mirror of
# count_segments.kara (counting starts).


def count_segments(s):
    count = 0
    for i in range(len(s)):
        if s[i] != " " and (i == 0 or s[i - 1] == " "):
            count += 1
    return count


def show(s):
    print(f"\"{s}\": {count_segments(s)}")


seed = 434


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("Hello, my name is John")
    show("Hello")
    show("")
    show(" ")
    show("     ")
    show("  leading and trailing  ")
    show("a  b   c    d")
    show("!@#$%^&*()_+-=',.:")
    show("x")
    show(" x ")
    symbols = "abcXYZ019!@#,.:-'"
    total = 0
    checksum = 0
    for _ in range(1000):
        length = next_random() % 61
        s = []
        for _ in range(length):
            if next_random() % 3 == 0:
                s.append(" ")
            else:
                s.append(symbols[next_random() % len(symbols)])
        n = count_segments("".join(s))
        total += n
        checksum = (checksum * 31 + n) % 1000000007
    print(f"1000 random strings: {total} segments, checksum {checksum}")


main()
