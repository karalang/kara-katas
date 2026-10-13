# LeetCode #472: Concatenated Words -- Python mirror of the ★ arm
# (concatenated_words.kara): shortest first, each word broken against
# the words before it.


def breaks(word, known):
    n = len(word)
    reach = [False] * (n + 1)
    reach[0] = True
    for end in range(1, n + 1):
        for start in range(0, end):
            if reach[start] and word[start:end] in known:
                reach[end] = True
                break
    return reach[n]


def find_all_concatenated_words_in_a_dict(words):
    order = sorted(words, key=len)
    known = set()
    found = []
    for word in order:
        if known and breaks(word, known):
            found.append(word)
        known.add(word)
    return found


# ---- test harness ---------------------------------------------------------

def show(words):
    got = sorted(find_all_concatenated_words_in_a_dict(words))
    line = "".join(" " + w for w in got)
    print(f"{len(words)} words -> {len(got)}:{line}")


seed = 472


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_words(letters, base, joined):
    seen = set()
    words = []
    tries = 0
    while len(words) < base and tries < 100:
        tries += 1
        size = 1 + next_random() % 4
        w = "".join(chr(97 + next_random() % letters) for _ in range(size))
        if w not in seen:
            seen.add(w)
            words.append(w)
    for _ in range(joined):
        parts = 2 + next_random() % 3
        w = ""
        for _ in range(parts):
            w += words[next_random() % len(words)]
        if next_random() % 4 == 0:
            w += chr(97 + next_random() % letters)
        if len(w) <= 30 and w not in seen:
            seen.add(w)
            words.append(w)
    return words


def main():
    show(["cat", "cats", "catsdogcats", "dog", "dogcatsdog", "hippopotamuses", "rat", "ratcatdogcat"])
    show(["cat", "dog", "catdog"])
    show(["a", "aa", "aaa", "aaaa"])
    show(["ab", "a", "b", "ba", "aba", "abab", "c"])
    show(["cat"])
    show(["xyz", "xy", "z", "yz", "x"])
    show(["abc", "ab", "cd", "abcd", "bcd", "a"])
    count = 300
    total_words = 0
    total = 0
    checksum = 0
    for _ in range(count):
        letters = 1 + next_random() % 3
        base = 2 + next_random() % 11
        joined = next_random() % 31
        words = random_words(letters, base, joined)
        got = sorted(find_all_concatenated_words_in_a_dict(words))
        total_words += len(words)
        total += len(got)
        for w in got:
            for b in w.encode():
                checksum = (checksum * 31 + b) % 1000000007
            checksum = (checksum * 31 + 1) % 1000000007
    print(f"{count} random lists, {total_words} words: {total} concatenated, checksum {checksum}")


main()
