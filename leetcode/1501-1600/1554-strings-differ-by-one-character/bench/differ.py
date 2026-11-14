# LeetCode #1554: Strings Differ by One Character -- bench: the ★ arm
# (every word entered once per place with that place blotted out) over 20
# lists of 1000 random words of 100 letters, built once, half of them with
# a pair planted that differs in one place, each asked 3 times. Python mirror of differ.kara.


def differ_by_one(dict_):
    seen = set()
    for word in dict_:
        for j in range(len(word)):
            pattern = word[:j] + "*" + word[j + 1:]
            if pattern in seen:
                return True
            seen.add(pattern)
    return False


seed = 1554


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    lists = []
    for l in range(20):
        dict_ = ["".join(alphabet[next_random() % 26] for _ in range(100)) for _ in range(1000)]
        if l % 2 == 1:
            at = next_random() % 1000
            place = next_random() % 100
            letters = list(dict_[at])
            letters[place] = "b" if letters[place] == "a" else "a"
            twin = next_random() % 1000
            dict_[twin] = "".join(letters)
        lists.append(dict_)
    yes = 0
    check = 0
    for p in range(3):
        for l in range(len(lists)):
            if differ_by_one(lists[l]):
                yes += 1
                check = mix(check, p * 20 + l)
    print(f"3 passes over 20 lists of 1000 words of 100 letters: {yes} true, checksum {check}")


main()
