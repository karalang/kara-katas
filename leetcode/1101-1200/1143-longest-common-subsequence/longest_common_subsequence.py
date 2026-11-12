# LeetCode #1143: Longest Common Subsequence -- mirrors
# longest_common_subsequence.kara (the ★ arm).


def longest_common_subsequence(text1, text2):
    a, b = text1, text2
    m, n = len(a), len(b)
    best = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                best[i][j] = best[i - 1][j - 1] + 1
            else:
                best[i][j] = max(best[i - 1][j], best[i][j - 1])
    return best[m][n]


seed = 1143


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_text(n, k):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(letters[next_random() % k] for _ in range(n))


def main():
    print(f"example 1: {longest_common_subsequence('abcde', 'ace')}")
    print(f"example 2: {longest_common_subsequence('abc', 'abc')}")
    print(f"example 3: {longest_common_subsequence('abc', 'def')}")
    print(f"one letter, alike: {longest_common_subsequence('a', 'a')}")
    print(f"one letter, not: {longest_common_subsequence('a', 'b')}")
    print(f"one inside the other: {longest_common_subsequence('xaxbxcx', 'abc')}")
    print(f"backwards: {longest_common_subsequence('abcdef', 'fedcba')}")
    print(f"crossing: {longest_common_subsequence('abab', 'baba')}")
    total = 0
    check = 0
    for i in range(2000):
        k = [2, 4, 26][i % 3]
        n1 = next_random() % 40 + 1
        n2 = next_random() % 40 + 1
        t1 = random_text(n1, k)
        t2 = random_text(n2, k)
        answer = longest_common_subsequence(t1, t2)
        total += answer
        check = (check * 131 + answer + 1) % 1000000007
    print(f"2000 random pairs: answers total {total}, checksum {check}")
    a = random_text(1000, 4)
    b = random_text(1000, 4)
    print(f"1000 and 1000 of 4 letters: {longest_common_subsequence(a, b)}")
    c = random_text(1000, 26)
    d = random_text(1000, 26)
    print(f"1000 and 1000 of 26 letters: {longest_common_subsequence(c, d)}")
    e = random_text(1000, 26)
    f = "".join("z" if i % 10 == 0 else ch for i, ch in enumerate(e))
    print(f"1000 letters, every tenth changed: {longest_common_subsequence(e, f)}")


main()
