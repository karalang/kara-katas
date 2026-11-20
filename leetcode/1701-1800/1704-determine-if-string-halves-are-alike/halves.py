# LeetCode #1704: Determine if String Halves Are Alike -- the Python
# mirror of the ★ arm (halves.kara): one pass, a vowel in the first half
# counted up and in the second down.

VOWELS = set(b"aeiouAEIOU")


def halves_are_alike(s):
    data = s.encode()
    half = len(data) // 2
    balance = 0
    for i, b in enumerate(data):
        if b in VOWELS:
            balance += 1 if i < half else -1
    return balance == 0


def next_random(state):
    state[0] = (state[0] * 1103515245 + 12345) % 2147483648
    return state[0] // 65536


def batch(count, most, seed):
    vowels = b"aeiouAEIOU"
    consonants = b"bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
    alike = 0
    check = 0
    for _ in range(count):
        n = 2 * (next_random(seed) % (most // 2) + 1)
        lean = next_random(seed) % 11
        out = bytearray()
        for _ in range(n):
            if next_random(seed) % 10 < lean:
                out.append(vowels[next_random(seed) % len(vowels)])
            else:
                out.append(consonants[next_random(seed) % len(consonants)])
        answer = halves_are_alike(out.decode())
        if answer:
            alike += 1
        check = (check * 31 + (1 if answer else 2) + n) % 1000000007
    print(f"{count} strings of up to {most} letters: {alike} alike, checksum {check}")


def main():
    # LeetCode's two examples, then capitals, no vowels, and two vowels
    for s in ["book", "textbook", "AbCdEfGhIo", "xyzw", "ae"]:
        print("true" if halves_are_alike(s) else "false")
    seed = [1704]
    batch(3000, 12, seed)
    batch(300, 100, seed)
    batch(3000, 1000, seed)


main()
