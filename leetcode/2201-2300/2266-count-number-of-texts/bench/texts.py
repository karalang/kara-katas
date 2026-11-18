# LeetCode #2266: Count Number of Texts -- Python mirror of the ★ arm
# (texts.kara) on the bench workload: ways[i] adds ways[i - j] for each
# run of j equal presses ending at i, up to 3, or 4 on `7` and `9`.
# Output is byte-identical to texts.kara.

MOD = 1000000007


def count_texts(pressed_keys):
    keys = pressed_keys.encode()
    n = len(keys)
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        key = keys[i - 1]
        most = 4 if key in (55, 57) else 3
        j = 1
        while j <= most and j <= i and keys[i - j] == key:
            ways[i] = (ways[i] + ways[i - j]) % MOD
            j += 1
    return ways[n]


# ---- bench harness ---------------------------------------------------------

seed = 2266


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    check = 0
    for t in range(40):
        keys = ["2", "79", "234", "23456789"][t % 4]
        pressed = "".join(keys[next_random() % len(keys)] for _ in range(100000))
        check = (check * 31 + count_texts(pressed)) % 1000000007
    print(f"40 strings of 10^5: checksum {check}")


main()
