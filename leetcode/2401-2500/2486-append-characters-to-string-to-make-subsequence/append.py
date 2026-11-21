# LeetCode #2486: Append Characters to String to Make Subsequence --
# Python mirror of append.kara: by two pointers.


def append_characters(s, t):
    matched = 0
    for c in s:
        if matched < len(t) and c == t[matched]:
            matched += 1
    return len(t) - matched


seed = 2486


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, kinds):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(letters[next_random() % kinds] for _ in range(n))


def main():
    cases = [("coaching", "coding"), ("abcde", "a"), ("z", "abcde"), ("a", "a"), ("a", "b"),
             ("abc", "abcdef"), ("abcd", "dcba"), ("ba", "ab")]
    for s, t in cases:
        print(f'"{s}", "{t}" -> {append_characters(s, t)}')
    long = random_word(100000, 26)
    backwards = long[::-1]
    print(f"10^5, t = s -> {append_characters(long, long)}")
    print(f"10^5, t reversed -> {append_characters(long, backwards)}")
    print(f"10^5 a, 10^5 b -> {append_characters('a' * 100000, 'b' * 100000)}")
    for kinds in [2, 26]:
        s = random_word(100000, kinds)
        t = random_word(100000, kinds)
        print(f"10^5 random of {kinds} letters -> {append_characters(s, t)}")
    check = 0
    for _ in range(3000):
        kinds = 1 + next_random() % 4
        s = random_word(1 + next_random() % 30, kinds)
        t = random_word(1 + next_random() % 30, kinds)
        check = (check * 31 + append_characters(s, t)) % 1000000007
    print(f"3000 random: checksum {check}")


if __name__ == "__main__":
    main()
