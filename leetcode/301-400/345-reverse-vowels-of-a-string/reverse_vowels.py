# LeetCode #345: Reverse Vowels of a String — Python mirror of reverse_vowels.kara (the ★ arm).


def is_vowel(c):
    return c in "aeiouAEIOU"


def reverse_vowels(s):
    cs = list(s)
    i = 0
    j = len(cs) - 1
    while i < j:
        if not is_vowel(cs[i]):
            i += 1
        elif not is_vowel(cs[j]):
            j -= 1
        else:
            cs[i], cs[j] = cs[j], cs[i]
            i += 1
            j -= 1
    return "".join(cs)


def report(s):
    r = reverse_vowels(s)
    print(f'"{s}" -> "{r}"')


def main():
    # The examples from the problem statement.
    report("IceCreAm")
    report("leetcode")

    # No vowels, one vowel, only vowels, and the two cases mixed.
    report("")
    report("a")
    report("xyz")
    report("aeiou")
    report("aA")
    report("Euston saw I was not Sue.")
    report("hello, world!")
    report("Programming in Kara")

    # Accented letters are not vowels here: the set is the ten ASCII letters.
    report("Kāra, señor, über alles")

    # Reversing twice is the identity, on a long string.
    long = "".join(chr((k * 7919) % 26 + 97) for k in range(100000))
    once = reverse_vowels(long)
    twice = reverse_vowels(once)
    vowels = sum(1 for c in long if is_vowel(c))
    changed = "true" if once != long else "false"
    restores = "true" if twice == long else "false"
    print(f"100000 letters, {vowels} vowels: changed by one reversal: {changed}, twice restores: {restores}")


main()
