# LeetCode #1461 Check If a String Contains All Binary Codes of Size K: a
# mirror of has_all_codes.kara.


def has_all_codes(s, k):
    need = 1 << k
    # the last k digits read as a number, each window marked once
    seen = [False] * need
    found = 0
    window = 0
    for i, b in enumerate(s.encode()):
        window = ((window << 1) | (b - ord("0"))) & (need - 1)
        if i + 1 >= k and not seen[window]:
            seen[window] = True
            found += 1
            if found == need:
                return True
    return False


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def draw(n, ones):
    return "".join("1" if next_random() % 8 < ones else "0" for _ in range(n))


def de_bruijn(k):
    seen = [False] * (1 << k)
    s = ["0"] * k
    seen[0] = True
    window = 0
    full = (1 << k) - 1
    while True:
        one = ((window << 1) | 1) & full
        zero = (window << 1) & full
        if not seen[one]:
            window = one
            s.append("1")
        elif not seen[zero]:
            window = zero
            s.append("0")
        else:
            break
        seen[window] = True
    return "".join(s)


def show(b):
    return "true" if b else "false"


def main():
    global seed
    f = has_all_codes
    e = [f("00110110", 2), f("0110", 1), f("0110", 2), f("0", 1), f("01", 1)]
    whole = de_bruijn(20)
    cut = whole[:-1]
    print(" ".join(show(x) for x in e + [f(whole, 20), f(cut, 20)]) + f" {len(whole)}")
    seed = 1461
    long = draw(500000, 4)
    most = 0
    for k in range(1, 21):
        if f(long, k):
            most = k
    print(f"5 * 10^5 digits: every code up to k = {most}")
    yes = 0
    check = 0
    for _ in range(3000):
        n = 1 + next_random() % 400
        k = 1 + next_random() % 8
        ones = 1 + next_random() % 7
        got = f(draw(n, ones), k)
        if got:
            yes += 1
        check = (check * 3 + (1 if got else 0)) % 1000000007
    print(f"3000 random strings: {yes} with every code, checksum {check}")


main()
