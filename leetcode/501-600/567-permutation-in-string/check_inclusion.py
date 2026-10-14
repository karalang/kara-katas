# LeetCode #567: Permutation in String -- Python mirror of the ★ arm (a
# sliding window); see check_inclusion.kara.


def check_inclusion(s1, s2):
    k = len(s1)
    if k > len(s2):
        return False
    need = [0] * 26
    for c in s1:
        need[ord(c) - ord("a")] += 1
    missing = k
    for i in range(len(s2)):
        enter = ord(s2[i]) - ord("a")
        if need[enter] > 0:
            missing -= 1
        need[enter] -= 1
        if i >= k:
            leave = ord(s2[i - k]) - ord("a")
            need[leave] += 1
            if need[leave] > 0:
                missing += 1
        if missing == 0:
            return True
    return False


# ---- test harness ---------------------------------------------------------

seed = 567


def step():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def show(s1, s2):
    print(f'"{s1}" in "{s2}": {"true" if check_inclusion(s1, s2) else "false"}')


def random_text(length, letters):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[step() % letters] for _ in range(length))


def main():
    show("ab", "eidbaooo")
    show("ab", "eidboaoo")
    show("abc", "ab")
    show("adc", "dcda")
    show("a", "a")
    show("a", "b")
    show("aab", "abab")
    show("aab", "abba")
    show("hello", "ooolleoooleh")
    show("xyz", "zyxaaaaaaa")
    show("xyz", "aaaaaaayzx")
    found = 0
    checksum = 0
    for _ in range(300):
        s1 = random_text(1 + step() % 5, 3)
        s2 = random_text(1 + step() % 30, 3)
        got = check_inclusion(s1, s2)
        if got:
            found += 1
        checksum = (checksum * 31 + (2 if got else 1)) % 1000000007
    print(f"300 random pairs: {found} found, checksum {checksum}")
    s1 = random_text(5000, 26)
    front = random_text(5000, 26)
    back = s1[::-1]
    print(f"10000 letters, planted at the end: {'true' if check_inclusion(s1, front + back) else 'false'}")
    least = "a"
    fewest = 5001
    for c in "abcdefghijklmnopqrstuvwxyz":
        n = s1.count(c)
        if n < fewest:
            fewest = n
            least = c
    spoiled = back[:4999] + least
    print(f"10000 letters, one letter off: {'true' if check_inclusion(s1, front + spoiled) else 'false'}")


main()
