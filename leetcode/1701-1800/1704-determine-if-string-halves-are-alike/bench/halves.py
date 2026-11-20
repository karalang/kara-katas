# LeetCode #1704: Determine if String Halves Are Alike -- the bench's
# Python mirror: the ★ arm on 1000 random strings of 1000 letters, all
# drawn first, each answered 400 times.

VOWELS = frozenset("aeiouAEIOU")


def halves_are_alike(s):
    # one pass: a vowel in the first half counted up and in the second down
    half = len(s) // 2
    balance = 0
    for i, c in enumerate(s):
        if c in VOWELS:
            balance += 1 if i < half else -1
    return balance == 0


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def main():
    count, rounds, n = 1000, 400, 1000
    seed = [1704]
    vowels = "aeiouAEIOU"
    consonants = "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    strings = []
    for _ in range(count):
        # each letter a vowel with a chance of its string's own, 0 to 10 in 10
        lean = next_random(seed) % 11
        out = []
        for _ in range(n):
            if next_random(seed) % 10 < lean:
                out.append(vowels[next_random(seed) % len(vowels)])
            else:
                out.append(consonants[next_random(seed) % len(consonants)])
        strings.append("".join(out))
    alike = 0
    check = 0
    for r in range(rounds):
        for s in strings:
            answer = halves_are_alike(s)
            if answer:
                alike += 1
            check = (check * 31 + (1 if answer else 2) + r) % 1000000007
    print(f"{count} strings of {n} letters, {rounds} rounds: {alike} alike, checksum {check}")


main()
