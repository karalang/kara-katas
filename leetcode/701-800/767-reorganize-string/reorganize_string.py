# LeetCode 767 — Reorganize String: the ★ arm in Python, same output.


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
    for k in [most] + [k for k in range(26) if k != most]:
        for _ in range(counts[k]):
            if place >= n:
                place = 1
            out[place] = chr(97 + k)
            place += 2
    return "".join(out)


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def verdict(s, answer):
    if not answer:
        return "none"
    ok = sorted(answer) == sorted(s) and all(a != b for a, b in zip(answer, answer[1:]))
    return "rearranged" if ok else f"WRONG {answer}"


def show(s):
    print(f"{s} -> {verdict(s, reorganize_string(s))}")


def main():
    global seed
    for s in ["aab", "aaab", "a", "aa", "ab", "aaabb", "aaabbb", "vvvlo",
              "aaaabbbcc", "aaaaabbbc", "aaaaaabbc"]:
        show(s)
    seed = 767
    possible = 0
    check = 0
    for rnd in range(300):
        n = 1 + next_random() % 40
        letters = 1 + next_random() % 5
        chars = []
        for _ in range(n):
            k = next_random() % (letters + 1)
            chars.append(chr(97 + (0 if k == letters else k)))
        s = "".join(chars)
        answer = reorganize_string(s)
        v = verdict(s, answer)
        if v == "rearranged":
            possible += 1
        elif v != "none":
            print(f"{s} -> {v}")
        check = (check * 31 + len(answer) + rnd) % 1000000007
    print(f"300 random strings: {possible} rearranged, checksum {check}")


main()
