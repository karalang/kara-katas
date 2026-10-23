# LeetCode #880: Decoded String at Index -- Python mirror of the ★ arm (the
# tape's length, then back from the end) and its test harness; prints the
# same output as decode_at_index.kara.


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


# ---- test harness ----------------------------------------------------------


def show(s, k):
    print(f's = "{s}", k = {k} -> "{decode_at_index(s, k)}"')


seed = 880


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def up_to(limit):
    x = next_random()
    y = next_random()
    return (x * 32768 + y) % limit + 1


def encoded(length, alphabet, bound):
    letters = "abcdefghijklmnopqrstuvwxyz"
    s = []
    size = 0
    for i in range(length):
        d = next_random() % 8 + 2
        if i > 0 and next_random() % 3 == 0 and size * d <= bound:
            s.append(str(d))
            size *= d
        elif size < bound:
            x = next_random() % alphabet
            s.append(letters[x])
            size += 1
    return "".join(s), size


def main():
    show("leet2code3", 10)
    show("ha22", 5)
    show("a2345678999999999999999", 1)
    show("leet2code3", 36)
    show("abc", 3)
    show("a2b3c4", 40)
    show("a2b3c4", 39)
    show("y959q969u3hb22odq595", 222280369)
    show("a2345678999999999999999", 1000000000)
    show("abcdefghijklmnopqrstuvwxyz9z9y9x9w9v9u9t9s9r9", 1000000000)
    total = 0
    check = 0
    for _ in range(3000):
        length = next_random() % 11 + 2
        s, size = encoded(length, 4, 200)
        k = up_to(size)
        answer = ord(decode_at_index(s, k))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"3000 cases of up to 12 characters: letters sum to {total}, checksum {check}")
    total = 0
    check = 0
    for _ in range(2000):
        length = next_random() % 99 + 2
        s, size = encoded(length, 26, 1000000000000000000)
        k = up_to(min(size, 1000000000))
        answer = ord(decode_at_index(s, k))
        total += answer
        check = (check * 131 + answer) % 1000000007
    print(f"2000 cases of up to 100 characters: letters sum to {total}, checksum {check}")


main()
