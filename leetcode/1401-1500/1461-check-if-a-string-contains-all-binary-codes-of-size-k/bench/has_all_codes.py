# LeetCode #1461 bench in Python: the ★ arm (the last k digits kept as a
# number, each window marked once) on the same 20 strings of 5 * 10^5
# digits, k from 11 to 20.


def has_all_codes(s, k):
    need = 1 << k
    seen = [False] * need
    found = 0
    window = 0
    for i, b in enumerate(s.encode()):
        window = ((window << 1) | (b - 48)) & (need - 1)
        if i + 1 >= k and not seen[window]:
            seen[window] = True
            found += 1
            if found == need:
                return True
    return False


seed = 1461


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    texts = []
    for _ in range(20):
        texts.append(bytearray(48 if next_random() % 2 == 0 else 49 for _ in range(500000)))
    check = 0
    for t in range(20):
        for k in range(11, 21):
            at = check % 500000
            texts[t][at] = 49 if texts[t][at] == 48 else 48
            s = texts[t].decode()
            all_ = has_all_codes(s, k)
            check = (check * 31 + (1 if all_ else 0) + k) % 1000000007
    print(f"20 strings of 5 * 10^5 digits, k from 11 to 20: checksum {check}")


main()
