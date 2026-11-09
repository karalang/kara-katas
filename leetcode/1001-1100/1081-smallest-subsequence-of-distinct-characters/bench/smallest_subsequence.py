# Benchmark: LeetCode #1081 Smallest Subsequence of Distinct Characters --
# the ★ arm. Mirrors smallest_subsequence.kara, .rs, .c and go-seq/.


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


seed = 1081


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def main():
    rounds = 100
    texts = []
    for t in range(2000):
        k = t % 26 + 1
        texts.append("".join(chr(97 + next_random() % k) for _ in range(1000)))
    kept = 0
    check = 0
    for r in range(rounds):
        for i in range(2000):
            out = smallest_subsequence(texts[(r * 7 + i) % 2000])
            kept += len(out)
            check = (check * 31 + out.encode()[len(out) // 2] + i) % 1000000007
    print(f"{rounds} rounds over 2000 texts of 1000 letters: {kept} letters kept, checksum {check}")


main()
