# LeetCode #2707: Extra Characters in a String -- the Python mirror of
# the star arm (extra.kara): from the end of the string back, the fewest
# extra characters in each suffix, either its first character left over
# or a dictionary word that starts it skipped whole.


def min_extra_char(s, dictionary):
    words = set(dictionary)
    n = len(s)
    best = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        best[i] = best[i + 1] + 1
        for j in range(i + 1, n + 1):
            if s[i:j] in words and best[j] < best[i]:
                best[i] = best[j]
    return best[0]


seed = 2707


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(ord("a") + next_random() % letters) for _ in range(n))


print(min_extra_char("leetscode", ["leet", "code", "leetcode"]))
print(min_extra_char("sayhelloworld", ["hello", "world"]))
print(min_extra_char("a", ["b"]))
print(min_extra_char("a" * 50, ["a" * 50]))
print(min_extra_char("a" * 50, ["aa", "aaa"]))
print(min_extra_char("ab" * 25, ["ba"]))
print(min_extra_char("abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwx", [chr(ord("a") + i) for i in range(0, 26, 2)]))
total = 0
check = 0
for _ in range(1000):
    n = next_random() % 50 + 1
    s = random_word(n, 3)
    dictionary = list(dict.fromkeys(random_word(next_random() % 5 + 1, 3) for _ in range(next_random() % 50 + 1)))
    extra = min_extra_char(s, dictionary)
    total += extra
    check = (check * 31 + extra) % 1000000007
print(f"1000 cases of 3 letters: extra characters sum to {total}, checksum {check}")
total = 0
check = 0
for _ in range(1000):
    n = next_random() % 50 + 1
    s = random_word(n, 26)
    dictionary = list(dict.fromkeys(random_word(next_random() % 3 + 1, 26) for _ in range(50)))
    extra = min_extra_char(s, dictionary)
    total += extra
    check = (check * 31 + extra) % 1000000007
print(f"1000 cases of 26 letters: extra characters sum to {total}, checksum {check}")
