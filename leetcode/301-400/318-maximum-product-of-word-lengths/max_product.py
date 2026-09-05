"""LeetCode #318: Maximum Product of Word Lengths — Python mirror of
max_product.kara. Same algorithm (26-bit letter masks, all pairs), same demo
cases, byte-identical output."""


def word_mask(w: str) -> int:
    m = 0
    for ch in w:
        m |= 1 << (ord(ch) - ord("a"))
    return m


def max_product(words: list[str]) -> int:
    n = len(words)
    masks = [word_mask(w) for w in words]
    lens = [len(w) for w in words]

    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            if masks[i] & masks[j] == 0:
                p = lens[i] * lens[j]
                if p > best:
                    best = p
    return best


def main() -> None:
    cases = [
        ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"],
        ["a", "ab", "abc", "d", "cd", "bcd", "abcd"],
        ["a", "aa", "aaa", "aaaa"],
        [],
        ["solo"],
        ["abc", "def"],
        ["abcdefghijklmnopqrstuvwxyz", "abcdefghijklmnopqrstuvwxyz"],
        ["aaaaaaaaaa", "bb", "cc", "bbcc"],
        ["eat", "tea", "tan", "ate", "nat", "bat"],
        ["qwer", "tyui", "opas", "dfgh"],
    ]

    for k, ws in enumerate(cases):
        print(f"case {k + 1}: [{' '.join(ws)}] -> {max_product(ws)}")


if __name__ == "__main__":
    main()
