# LeetCode #1576: Replace All ?'s to Avoid Consecutive Repeating
# Characters -- bench: the ★ arm (the first of a, b, c that fits, in a
# Vec[char]) over 20 strings of 500000 characters, half of them '?', built
# once; then 4 rounds answering all 20, each answer folded to its count of
# 'a's.


def modify_string(s):
    cs = list(s)
    n = len(cs)
    for i in range(n):
        if cs[i] == "?":
            for c in "abc":
                if (i == 0 or cs[i - 1] != c) and (i + 1 == n or cs[i + 1] != c):
                    cs[i] = c
                    break
    return "".join(cs)


seed = 1576


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def mix(check, x):
    return (check * 31 + x + 1) % 1000000007


def main():
    n = 500000
    strings = []
    for _ in range(20):
        s = []
        last = " "
        for _ in range(n):
            if next_random() % 2 == 0:
                s.append("?")
                last = "?"
            else:
                k = next_random() % 26
                if chr(ord("a") + k) == last:
                    k = (k + 1) % 26
                c = chr(ord("a") + k)
                s.append(c)
                last = c
        strings.append("".join(s))
    check = 0
    total = 0
    for _ in range(4):
        for s in strings:
            a = modify_string(s).count("a")
            total += a
            check = mix(check, a)
    print(f"80 answers over 20 strings of {n} characters: 'a' total {total}, checksum {check}")


main()
