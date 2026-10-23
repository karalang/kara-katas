# LeetCode #880 bench: Python mirror of decode_at_index.kara (the ★ arm,
# the tape's length, then back from the end) on the same 1,000,000 queries.

def decode_at_index(s, k):
    size = 0
    for c in s:
        if c.isdigit():
            size *= int(c)
        else:
            size += 1
    i = len(s) - 1
    while True:
        k %= size
        if k == 0 and not s[i].isdigit():
            return s[i]
        if s[i].isdigit():
            size //= int(s[i])
        else:
            size -= 1
        i -= 1


seed = 880


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit + 1


def encoded(length):
    letters = "abcdefghijklmnopqrstuvwxyz"
    bound = 1000000000000000000
    s = []
    size = 0
    for i in range(length):
        d = next_random() % 8 + 2
        if i > 0 and next_random() % 3 == 0 and size * d <= bound:
            s.append(str(d))
            size *= d
        elif size < bound:
            x = next_random() % 26
            s.append(letters[x])
            size += 1
    return "".join(s), size


def main():
    strings = []
    sizes = []
    for _ in range(1000):
        length = next_random() % 99 + 2
        s, size = encoded(length)
        strings.append(s)
        sizes.append(size)
    total = 0
    check = 0
    for q in range(1000000):
        j = q % 1000
        k = up_to(min(sizes[j], 1000000000))
        answer = ord(decode_at_index(strings[j], k))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"1000000 queries over 1000 strings: letters sum to {total}, checksum {check}")


main()
