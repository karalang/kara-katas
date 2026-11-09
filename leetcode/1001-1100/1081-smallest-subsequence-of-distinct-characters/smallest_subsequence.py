# LeetCode #1081: Smallest Subsequence of Distinct Characters -- mirrors
# smallest_subsequence.kara (the ★ arm, a stack of the answer so far)
# and its harness; the output is byte-identical.


def smallest_subsequence(s):
    data = s.encode()
    last = [0] * 26
    for i in range(len(data)):
        last[data[i] - 97] = i
    placed = [False] * 26
    stack = []
    for i in range(len(data)):
        b = data[i]
        if placed[b - 97]:
            continue
        while stack:
            top = stack[-1]
            if top > b and last[top - 97] > i:
                placed[top - 97] = False
                stack.pop()
            else:
                break
        stack.append(b)
        placed[b - 97] = True
    return bytes(stack).decode()


seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def fold(h, text):
    for b in text.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    global seed
    cases = [
        "bcabc",
        "cbacdcbc",
        "a",
        "aaaa",
        "abcabc",
        "cba",
        "bcac",
        "leetcode",
        "zyxzyxzyx",
        "ecbacba",
        "abacb",
        "thesqtitxyetpxloeevdeqifkz",
    ]
    for s in cases:
        print(f"{s} -> {smallest_subsequence(s)}")
    seed = 1081
    h = 0
    total = 0
    for t in range(300):
        n = next_random() % 1000 + 1
        k = t % 26 + 1
        out = smallest_subsequence(random_text(n, k))
        total += len(out)
        h = fold(h, out)
    print(f"300 random strings: {total} letters kept, checksum {h}")
    long = []
    for i in range(1000):
        long.append(chr(ord("z") - i % 26))
    print(f"1000 letters, the alphabet backwards -> {smallest_subsequence(''.join(long))}")


main()
