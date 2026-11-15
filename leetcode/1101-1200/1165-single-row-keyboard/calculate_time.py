# LeetCode #1165: Single-Row Keyboard -- a Python mirror of the ★ arm (a
# table of each letter's place) and its test harness; the output is
# byte-identical to calculate_time.kara's.


def calculate_time(keyboard, word):
    place = [0] * 26
    for i, c in enumerate(keyboard.encode()):
        place[c - 97] = i
    at = 0
    time = 0
    for c in word.encode():
        nxt = place[c - 97]
        time += abs(nxt - at)
        at = nxt
    return time


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_keyboard():
    b = [chr(97 + i) for i in range(26)]
    for i in range(25, 0, -1):
        j = next_random() % (i + 1)
        b[i], b[j] = b[j], b[i]
    return "".join(b)


def word(length, k):
    return "".join(chr(97 + next_random() % k) for _ in range(length))


def main(solve):
    global seed
    az = "abcdefghijklmnopqrstuvwxyz"
    cases = [(az, "cba"), ("pqrstuvwxyzabcdefghijklmno", "leetcode"), (az, "a"), (az, "z"),
             (az, "zzzz"), (az, az), ("zyxwvutsrqponmlkjihgfedcba", az)]
    for k, w in cases:
        print(f"{k} {w} -> {solve(k, w)}")
    seed = 1165
    total = 0
    check = 0
    for _ in range(2000):
        keyboard = random_keyboard()
        k = 1 + next_random() % 26
        w = word(1 + next_random() % 40, k)
        t = solve(keyboard, w)
        total += t
        check = (check * 31 + t) % 1000000007
    print(f"2000 random words: total {total}, checksum {check}")
    keyboard = random_keyboard()
    print(f"10000 letters: {solve(keyboard, word(10000, 26))}")
    print(f"10000 letters a and z: {solve(az, 'az' * 5000)}")


if __name__ == "__main__":
    main(calculate_time)
