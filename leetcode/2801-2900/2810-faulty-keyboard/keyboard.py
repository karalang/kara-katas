# LeetCode #2810: Faulty Keyboard -- the Python mirror of the ★ arm: each
# letter pushed on, each i turning the screen round.


def final_string(s):
    screen = ""
    for c in s:
        if c == "i":
            screen = screen[::-1]
        else:
            screen += c
    return screen


seed = 2810


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def typed(m, letters):
    s = ""
    while len(s) < m:
        c = letters[next_random() % len(letters)]
        if not (s == "" and c == "i"):
            s += c
    return s


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    print(final_string("string"))
    print(final_string("poiinter"))
    print(final_string("abcdefghjklmnopqrstuvwxyz" * 4))
    half = "".join("ai" if k % 2 == 0 else "bi" for k in range(50))
    print(final_string("z" + half))
    total = 0
    check = 0
    for _ in range(3000):
        s = final_string(typed(next_random() % 10 + 1, "abi"))
        total += len(s)
        check = (check * 31 + digest(s)) % 1000000007
    print(f"3000 short strings: lengths sum to {total}, checksum {check}")
    total = 0
    check = 0
    pool = "abcdefghijklmnopqrstuvwxyz" + "i" * 25
    for _ in range(50):
        s = final_string(typed(next_random() % 100 + 1, pool))
        total += len(s)
        check = (check * 31 + digest(s)) % 1000000007
    print(f"50 long strings: lengths sum to {total}, checksum {check}")


main()
