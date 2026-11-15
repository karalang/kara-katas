# LeetCode #1165: Single-Row Keyboard -- Python mirror of the Kāra ★ arm:
# each letter's place in a table of 26, then the moves summed from place 0.


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


seed = 1165


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    keyboards = []
    words = []
    for _ in range(16):
        b = [chr(97 + i) for i in range(26)]
        for i in range(25, 0, -1):
            j = next_random() % (i + 1)
            b[i], b[j] = b[j], b[i]
        keyboards.append("".join(b))
        words.append("".join(chr(97 + next_random() % 26) for _ in range(10000)))
    total = 0
    check = 0
    for _ in range(5000):
        for k in range(16):
            frm = next_random() % 5000
            t = calculate_time(keyboards[k], words[k][frm:])
            total += t
            check = (check * 31 + t) % 1000000007
    print(f"5000 rounds over 16 words of 10^4 letters: total {total}, checksum {check}")


main()
