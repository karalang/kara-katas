# LeetCode #2266: Count Number of Texts -- Python mirror of the ★ arm
# (texts.kara): ways[i] adds ways[i - j] for each run of j equal presses
# ending at i, up to 3, or 4 on `7` and `9`. Output is byte-identical to
# texts.kara.

MOD = 1000000007


def count_texts(pressed_keys):
    keys = pressed_keys.encode()
    n = len(keys)
    ways = [0] * (n + 1)
    ways[0] = 1
    for i in range(1, n + 1):
        key = keys[i - 1]
        most = 4 if key in (ord("7"), ord("9")) else 3
        j = 1
        while j <= most and j <= i and keys[i - j] == key:
            ways[i] = (ways[i] + ways[i - j]) % MOD
            j += 1
    return ways[n]


# ---- test harness ---------------------------------------------------------

seed = 2266


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def presses(length, keys):
    return "".join(keys[next_random() % len(keys)] for _ in range(length))


def main():
    for keys in ["22233", "222222222222222222222222222222222222", "8", "2222", "7777", "232323", "77777"]:
        print(f"{keys} -> {count_texts(keys)}")
    check = 0
    for t in range(2000):
        length = next_random() % 40 + 1
        pressed = presses(length, ["2", "79", "27", "234", "23456789"][t % 5])
        check = (check * 31 + count_texts(pressed)) % 1000000007
    print(f"2000 presses: checksum {check}")
    sevens = "7" * 100000
    twos = "2" * 100000
    mixed = presses(100000, "79")
    answers = [count_texts(sevens), count_texts(twos), count_texts(mixed)]
    print(f"10^5 presses: [{', '.join(str(a) for a in answers)}]")


main()
