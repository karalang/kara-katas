# LeetCode #2381: Shifting Letters II -- Python mirror of the ★ arm, a
# difference array.


def shifting_letters(s, shifts):
    n = len(s)
    diff = [0] * (n + 1)
    for start, end, direction in shifts:
        step = 1 if direction == 1 else -1
        diff[start] += step
        diff[end + 1] -= step
    out = []
    total = 0
    for i in range(n):
        total += diff[i]
        out.append(chr(97 + (ord(s[i]) - 97 + total) % 26))
    return "".join(out)


seed = 2381


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def letters_checksum(s):
    check = 0
    for c in s:
        check = (check * 31 + ord(c) - 97) % 1000000007
    return check


def main():
    print(shifting_letters("abc", [[0, 1, 0], [1, 2, 1], [0, 2, 1]]))
    print(shifting_letters("dztz", [[0, 0, 0], [1, 1, 1]]))
    print(shifting_letters("a", [[0, 0, 0]]))
    n = 50000
    long = "".join(chr(97 + next_random() % 26) for _ in range(n))
    short = []
    for _ in range(n):
        start = next_random() % n
        end = min(start + next_random() % 100, n - 1)
        short.append([start, end, next_random() % 2])
    whole = [[0, n - 1, i % 3 % 2] for i in range(200)]
    print(f"{letters_checksum(shifting_letters(long, short))} {letters_checksum(shifting_letters(long, whole))}")
    check = 0
    same = 0
    for _ in range(2000):
        length = 1 + next_random() % 30
        s = "".join(chr(97 + next_random() % 26) for _ in range(length))
        count = next_random() % 31
        shifts = []
        for _ in range(count):
            a = next_random() % length
            b = next_random() % length
            shifts.append([min(a, b), max(a, b), next_random() % 2])
        t = shifting_letters(s, shifts)
        check = (check * 31 + letters_checksum(t)) % 1000000007
        if t == s:
            same += 1
    print(f"2000 strings: checksum {check}, {same} come back unchanged")


main()
