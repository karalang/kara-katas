# LeetCode #1119: Remove Vowels from a String -- Python mirror of the ★ arm.

seed = 1119


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def remove_vowels(s):
    return "".join(c for c in s if c not in "aeiou")


def random_text(n, odds):
    out = []
    for _ in range(n):
        if next_random() % odds == 0:
            out.append("aeiou"[next_random() % 5])
        else:
            out.append("bcdfghjklmnpqrstvwxyz"[next_random() % 21])
    return "".join(out)


def main():
    cases = ["leetcodeisacommunityforcoders", "aeiou", "b", "a", "abcdefghijklmnopqrstuvwxyz", "abba", "baaab", "uuuuuu", "rhythm"]
    for s in cases:
        print(f'{s} -> "{remove_vowels(s)}"')
    kept = check = 0
    for i in range(2000):
        n = next_random() % 1000 + 1
        r = remove_vowels(random_text(n, i % 5 + 2))
        kept += len(r)
        for c in r:
            check = (check * 31 + ord(c)) % 1000000007
    print(f"2000 random texts: {kept} letters kept, checksum {check}")


main()
