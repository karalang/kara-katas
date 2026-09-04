# LeetCode #316: Remove Duplicate Letters — Python mirror of the demo in
# remove_duplicate_letters.kara (monotone stack). Same cases, same sink.

def remove_duplicate_letters(s: str) -> str:
    last = {c: i for i, c in enumerate(s)}
    stack = []
    on_stack = set()
    for i, c in enumerate(s):
        if c in on_stack:
            continue
        while stack and stack[-1] > c and last[stack[-1]] > i:
            on_stack.discard(stack.pop())
        stack.append(c)
        on_stack.add(c)
    return "".join(stack)


def main():
    cases = [
        "bcabc", "cbacdcbc", "a", "aaaa", "abcabc", "cba", "bbcaac",
        "leetcode", "zyxzyxzyx", "ecbacba", "bcac",
    ]
    acc = 0
    for c, s in enumerate(cases):
        r = remove_duplicate_letters(s)
        for ch in r:
            acc = (acc * 131 + ord(ch)) % 1000000007
        print(f"case {c}: {s} -> {r}")
    print(f"sink: {acc}")


if __name__ == "__main__":
    main()
