# LeetCode #2785: Sort Vowels in a String -- the bench in Python: the ★
# arm over 20 strings of 10^5 letters from all 52, all drawn first, then
# each answered 10 times.


def is_vowel(c):
    return c in "aeiouAEIOU"


def sort_vowels(s):
    vowels = sorted(c for c in s if is_vowel(c))
    out = []
    nxt = 0
    for c in s:
        if is_vowel(c):
            out.append(vowels[nxt])
            nxt += 1
        else:
            out.append(c)
    return "".join(out)


seed = 2785


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(letters[next_random() % len(letters)] for _ in range(n))


def main():
    count = 20
    rounds = 10
    every = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    cases = [random_text(100000, every) for _ in range(count)]
    check = 0
    for r in range(rounds):
        for s in cases:
            t = sort_vowels(s)
            for b in t.encode():
                check = (check * 31 + b) % 1000000007
            check = (check + r) % 1000000007
    print(f"{count} strings of 10^5, {rounds} rounds: checksum {check}")


main()
