# LeetCode 767 — Reorganize String: benchmark, the ★ arm in Python.
# Sixty-four random strings of 500 letters, built once; 400,000 rounds
# each reorganize the next of them.


def reorganize_string(s):
    n = len(s)
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    most = 0
    for k in range(1, 26):
        if counts[k] > counts[most]:
            most = k
    if counts[most] > (n + 1) // 2:
        return ""
    out = [""] * n
    place = 0
    for step in range(27):
        k = most if step == 0 else step - 1
        if step > 0 and k == most:
            continue
        for _ in range(counts[k]):
            if place >= n:
                place = 1
            out[place] = chr(97 + k)
            place += 2
    return "".join(out)


seed = 767


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 400000
    pool = []
    for _ in range(64):
        letters = 1 + next_random() % 26
        chars = []
        for _ in range(500):
            k = next_random() % (letters + 1)
            chars.append(chr(97 + (0 if k == letters else k)))
        pool.append("".join(chars))
    possible = 0
    check = 0
    for rnd in range(rounds):
        answer = reorganize_string(pool[rnd % 64])
        letter = 0
        if answer:
            possible += 1
            letter = ord(answer[rnd % 500])
        check = (check * 31 + len(answer) + letter) % 1000000007
    print(f"{rounds} strings of 500 letters: {possible} rearranged, checksum {check}")


main()
