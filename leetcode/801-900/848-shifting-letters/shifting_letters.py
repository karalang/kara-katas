# LeetCode #848: Shifting Letters -- Python mirror of the ★ arm and its harness.


def shifting_letters(s, shifts):
    b = bytearray(s.encode())
    shift = 0
    for i in range(len(b) - 1, -1, -1):
        shift = (shift + shifts[i]) % 26
        b[i] = ord('a') + (b[i] - ord('a') + shift) % 26
    return b.decode()


def show(s, shifts):
    print(f"\"{s}\", [{', '.join(map(str, shifts))}] -> \"{shifting_letters(s, shifts)}\"")


seed = 848


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def digest(text):
    h = 0
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    for s, sh in [("abc", [3, 5, 9]), ("aaa", [1, 2, 3]), ("z", [1]), ("a", [0]), ("a", [25]),
                  ("a", [26]), ("az", [1, 1]), ("zz", [0, 1]),
                  ("abcdefghijklmnopqrstuvwxyz", [1] * 26),
                  ("abc", [1000000000] * 3), ("hello", [0] * 5), ("kara", [52, 26, 78, 1])]:
        show(s, sh)
    long = ''.join(chr(ord('a') + next_random() % 26) for _ in range(100000))
    a = shifting_letters(long, [1000000000] * 100000)
    print(f"10^5 letters, every shift 10^9: starts \"{a[:12]}\", digest {digest(a)}")
    b = shifting_letters(long, [1] * 100000)
    print(f"10^5 letters, every shift 1: starts \"{b[:12]}\", digest {digest(b)}")
    rnd = [next_random() * 31 % 1000000001 for _ in range(100000)]
    c = shifting_letters(long, rnd)
    print(f"10^5 letters, random shifts: starts \"{c[:12]}\", digest {digest(c)}")
    check = 0
    for _ in range(500):
        n = 1 + next_random() % 30
        s = []
        shifts = []
        for _ in range(n):
            s.append(chr(ord('a') + next_random() % 26))
            shifts.append(next_random() * 4657 % 1000000001 if next_random() % 4 == 0 else next_random() % 30)
        check = (check * 7 + digest(shifting_letters(''.join(s), shifts))) % 1000000007
    print(f"500 random strings: checksum {check}")


main()
