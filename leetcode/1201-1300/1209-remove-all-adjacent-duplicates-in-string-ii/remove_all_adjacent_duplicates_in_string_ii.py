# LeetCode #1209: Remove All Adjacent Duplicates in String II -- a Python
# mirror of the ★ arm: a stack of runs, each a letter and how many times
# it has come in a row; a run that reaches k is popped.


def remove_duplicates(s, k):
    runs = []
    for c in s:
        if runs and runs[-1][0] == c:
            runs[-1][1] += 1
            if runs[-1][1] == k:
                runs.pop()
        else:
            runs.append([c, 1])
    return "".join(c * n for c, n in runs)


seed = 1209


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def digest(s):
    h = 0
    for b in s.encode():
        h = (h * 131 + b) % 1000000007
    return h


def main():
    cases = [
        ("abcd", 2),
        ("deeedbbcccbdaa", 3),
        ("pbbcggttciiippooaais", 2),
        ("aaa", 4),
        ("aaaa", 2),
        ("aaaaa", 2),
        ("yfttttfbbbbnnnnffbgffffgbbbbgssssgthyyyy", 4),
        ("abccbaabccba", 2),
    ]
    for s, k in cases:
        print(f'{s} {k}: "{remove_duplicates(s, k)}"')
    changed = left = check = 0
    for _ in range(1000):
        n = next_random() % 20 + 1
        letters = next_random() % 2 + 2
        k = next_random() % 3 + 2
        s = random_text(n, letters)
        answer = remove_duplicates(s, k)
        if answer != s:
            changed += 1
        left += len(answer)
        check = (check * 131 + digest(answer) + len(answer)) % 1000000007
    print(f"1000 small cases: {changed} changed, {left} letters left, checksum {check}")
    s = random_text(100000, 2)
    answer = remove_duplicates(s, 2)
    print(f"100000 random a and b, k 2: {len(answer)} left, digest {digest(answer)}")
    s = random_text(100000, 3)
    answer = remove_duplicates(s, 3)
    print(f"100000 random a, b and c, k 3: {len(answer)} left, digest {digest(answer)}")
    half = random_text(50000, 26)
    answer = remove_duplicates(half + half[::-1], 2)
    print(f"50000 letters and their reverse, k 2: {len(answer)} left")
    s = "c" * 3000 + "b" * 5000 + "a" * 10000 + "b" * 5000 + "c" * 7001
    answer = remove_duplicates(s, 10000)
    print(f'runs of c, b, a, b, c, k 10000: "{answer}"')


main()
