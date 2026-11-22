# LeetCode #2716: Minimize String Length -- the ★ arm (minimize.kara) in
# Python: the number of distinct letters, counted by a set.


def minimized_string_length(s):
    return len(set(s))


seed = 2716


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


print(minimized_string_length("aaabc"))
print(minimized_string_length("cbbd"))
print(minimized_string_length("dddaaa"))
print(minimized_string_length("q"))
print(minimized_string_length("abcdefghijklmnopqrstuvwxyz"))
print(minimized_string_length("a" * 100))
print(minimized_string_length(("zyxwvutsrqponmlkjihgfedcba" * 4)[:100]))
seed = 2716
total = 0
check = 0
for _ in range(5000):
    n = next_random() % 100 + 1
    letters = next_random() % 26 + 1
    s = random_word(n, letters)
    length = minimized_string_length(s)
    total += length
    check = (check * 31 + length) % 1000000007
print(f"5000 strings: lengths sum to {total}, checksum {check}")
