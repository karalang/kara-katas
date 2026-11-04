# LeetCode #1047: Remove All Adjacent Duplicates In String -- Python mirror
# of remove_dups.kara.
#
# The same stack: push each letter unless it cancels the one on top.


def remove_duplicates(s):
    stack = []
    for c in s:
        if stack and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_string(n, k):
    return "".join(chr(ord("a") + next_random() % k) for _ in range(n))


def fold_answer(answer, acc):
    acc[0] += len(answer)
    if not answer:
        acc[1] += 1
    for c in answer:
        acc[2] = (acc[2] * 31 + ord(c)) % 1000000007
    acc[2] = (acc[2] * 31 + 1) % 1000000007


def main():
    global seed
    examples = ["abbaca", "azxxzy", "a", "aa", "aaa", "abba", "abccba", "abcd", "aabbcc", "abcddcbaz"]
    for s in examples:
        print(f'"{s}" -> "{remove_duplicates(s)}"')
    cases = 0
    acc = [0, 0, 0]
    for n in range(1, 9):
        for code in range(3 ** n):
            s = ""
            c = code
            for _ in range(n):
                s += chr(ord("a") + c % 3)
                c //= 3
            cases += 1
            fold_answer(remove_duplicates(s), acc)
    print(f"every string of 1 to 8 of a, b, c: {cases} cases, length {acc[0]}, {acc[1]} empty, checksum {acc[2]}")
    seed = 1047
    for k in [3, 26]:
        acc = [0, 0, 0]
        for _ in range(1000):
            n = next_random() % 200 + 1
            fold_answer(remove_duplicates(random_string(n, k)), acc)
        print(f"1000 random strings of {k} letters: length {acc[0]}, {acc[1]} empty, checksum {acc[2]}")
    alternating = "ab" * 5000
    run = "a" * 10001
    half = [chr(ord("a") + (i * 7 + i // 26) % 26) for i in range(5000)]
    mirrored = "".join(half) + "".join(reversed(half))
    for name, s in [("ab x 5000", alternating), ("a x 10001", run), ("5000 letters and their reverse", mirrored)]:
        acc = [0, 0, 0]
        fold_answer(remove_duplicates(s), acc)
        print(f"{name}: length {acc[0]}, checksum {acc[2]}")


main()
