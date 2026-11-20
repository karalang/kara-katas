# LeetCode #1662: Check If Two String Arrays are Equivalent -- the Python
# mirror of the ★ arm (two cursors, one in each array).


def array_strings_are_equal(word1, word2):
    w1 = i1 = 0
    w2 = i2 = 0
    while w1 < len(word1) and w2 < len(word2):
        a = word1[w1]
        b = word2[w2]
        if a[i1] != b[i2]:
            return False
        i1 += 1
        i2 += 1
        if i1 == len(a):
            w1 += 1
            i1 = 0
        if i2 == len(b):
            w2 += 1
            i2 = 0
    return w1 == len(word1) and w2 == len(word2)


# ---- the harness: the same in every arm --------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, kinds):
    return "".join(chr(ord("a") + next_random() % kinds) for _ in range(n))


def cut(text, gap):
    words = []
    start = 0
    for i in range(1, len(text)):
        if next_random() % gap == 0:
            words.append(text[start:i])
            start = i
    words.append(text[start:])
    return words


def spoil(text):
    at = next_random() % len(text)
    kind = next_random() % 3
    if kind == 0:
        new = "b" if text[at] == "a" else "a"
        return text[:at] + new + text[at + 1:]
    if kind == 1 and len(text) > 1:
        return text[:at] + text[at + 1:]
    return text + "a"


def batch(count, longest, gap):
    equal = 0
    check = 0
    letters = 0
    for k in range(count):
        n = next_random() % longest + 1
        kinds = next_random() % 3 + 1
        text = random_text(n, kinds)
        other = text if k % 2 == 0 else spoil(text)
        word1 = cut(text, gap)
        word2 = cut(other, gap)
        letters += len(text) + len(other)
        answer = array_strings_are_equal(word1, word2)
        if answer:
            equal += 1
        check = (check * 31 + (2 if answer else 1) + len(word1) + len(word2)) % 1000000007
    print(f"{count} pairs of up to {longest} letters ({letters} in all): {equal} equal, checksum {check}")


def show(b):
    print("true" if b else "false")


show(array_strings_are_equal(["ab", "c"], ["a", "bc"]))
show(array_strings_are_equal(["a", "cb"], ["ab", "c"]))
show(array_strings_are_equal(["abc", "d", "defg"], ["abcddefg"]))
show(array_strings_are_equal(["kara"], ["k", "a", "r", "a"]))
show(array_strings_are_equal(["ab"], ["a", "b", "c"]))
show(array_strings_are_equal(["xyz", "w"], ["xy", "zv"]))
seed = 1662
batch(3000, 12, 3)
batch(300, 1000, 50)
batch(10, 100000, 1000)
