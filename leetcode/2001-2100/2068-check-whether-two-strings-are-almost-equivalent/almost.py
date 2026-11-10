# LeetCode #2068: Check Whether Two Strings are Almost Equivalent -- the
# Python mirror of almost.kara (the ★ arm): one list of 26 differences, the
# first word counted up and the second down, none past 3 either way.


def check_almost_equivalent(word1, word2):
    diff = [0] * 26
    for b in word1.encode():
        diff[b - 97] += 1
    for b in word2.encode():
        diff[b - 97] -= 1
    return all(abs(d) <= 3 for d in diff)


# ---- test harness ----------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def word_of(n, k, seed):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(letters[next_random(seed) % k] for _ in range(n))


def changed(word, changes, k, seed):
    letters = "abcdefghijklmnopqrstuvwxyz"
    out = list(word)
    for _ in range(changes):
        i = next_random(seed) % len(out)
        out[i] = letters[next_random(seed) % k]
    return "".join(out)


def main():
    examples = [("aaaa", "bccb"), ("abcdeef", "abaaacc"), ("cccddabba", "babababab"), ("a", "b"), ("aaa", "bbb"), ("aaaa", "aaab"), ("zzzzzzzz", "zzzzaaaa"), ("abc", "cba")]
    for a, b in examples:
        print(f"{a} {b} -> {'true' if check_almost_equivalent(a, b) else 'false'}")
    seed = [2068]
    yes = 0
    check = 0
    for _ in range(1000):
        n = next_random(seed) % 100 + 1
        k = next_random(seed) % 26 + 1
        a = word_of(n, k, seed)
        b = word_of(n, k, seed) if next_random(seed) % 2 == 0 else changed(a, next_random(seed) % 25, k, seed)
        ok = check_almost_equivalent(a, b)
        if ok:
            yes += 1
        check = (check * 2 + (1 if ok else 0)) % 1000000007
    print(f"1000 pairs: {yes} almost equivalent, checksum {check}")


main()
