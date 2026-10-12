# LeetCode #443: String Compression -- mirror of compress.kara (reading
# and writing in place).


def compress(chars):
    n = len(chars)
    read = 0
    write = 0
    while read < n:
        c = chars[read]
        start = read
        while read < n and chars[read] == c:
            read += 1
        chars[write] = c
        write += 1
        count = read - start
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write


# Compresses the characters of s and returns the compressed text.
def compressed(s):
    chars = list(s)
    length = compress(chars)
    return "".join(chars[:length])


def show(s):
    out = compressed(s)
    print(f"\"{s}\": {len(out)} \"{out}\"")


seed = 443


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    show("aabbccc")
    show("a")
    show("abbbbbbbbbbbb")
    show("aaaaaaaaaa")
    show("abc")
    show("1111222")
    show("@@@!!a##")
    show("z" * 100)
    # 300 random strings of 1 to 300 characters, in runs of 1 to 1, 3,
    # 15 or 120 from a three-letter alphabet, so that neighbouring runs
    # often share a letter and merge.
    length = 0
    checksum = 0
    for _ in range(300):
        n = 1 + next_random() % 300
        longest = [1, 3, 15, 120][next_random() % 4]
        s = []
        while len(s) < n:
            c = chr(97 + next_random() % 3)
            run = 1 + next_random() % longest
            for _ in range(run):
                if len(s) < n:
                    s.append(c)
        out = compressed("".join(s))
        length += len(out)
        for c in out:
            checksum = (checksum * 31 + ord(c)) % 1000000007
    print(f"300 random strings: compressed length {length}, checksum {checksum}")


main()
