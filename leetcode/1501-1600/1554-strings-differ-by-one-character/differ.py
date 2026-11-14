# LeetCode #1554: Strings Differ by One Character -- the Python mirror of
# differ.kara, the ★ arm: every word entered once per place with that
# place blotted out, a repeat being the pair. Prints byte-identical output.


def differ_by_one(dict_):
    seen = set()
    for word in dict_:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j + 1:]
            if pattern in seen:
                return True
            seen.add(pattern)
    return False


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def show(answer):
    return "true" if answer else "false"


def batch(count, most, longest, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    check = 0
    yes = 0
    for _ in range(count):
        want = next_random() % most + 1
        length = next_random() % longest + 1
        own = next_random() % letters + 1
        room = 1
        for _ in range(length):
            room = min(room * own, want)
        taken = set()
        dict_ = []
        while len(dict_) < min(want, room):
            word = "".join(alphabet[next_random() % own] for _ in range(length))
            if word not in taken:
                taken.add(word)
                dict_.append(word)
        answer = differ_by_one(dict_)
        if answer:
            yes += 1
        check = mix(check, 1 if answer else 0)
    print(f"{count} lists of up to {most} words of up to {longest} letters: {yes} true, checksum {check}")


def main():
    global seed
    examples = [
        ["abcd", "acbd", "aacd"],
        ["ab", "cd", "yz"],
        ["abcd", "cccc", "abyd", "abab"],
        ["a"],
        ["a", "b"],
        ["ab", "ba"],
        ["abc", "xbz", "xyc", "ayz"],
        ["aaaa", "aaab", "zzzz"],
    ]
    for d in examples:
        print(f"[{', '.join(d)}] -> {show(differ_by_one(d))}")
    seed = 1554
    batch(3000, 8, 5, 3)
    batch(300, 1000, 20, 4)
    batch(30, 10000, 10, 26)


main()
