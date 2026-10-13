# LeetCode #466: Count The Repetitions -- mirror of count_repetitions.kara
# (the star arm: find the cycle).


def get_max_repetitions(s1, n1, s2, n2):
    a = list(s1)
    b = list(s2)
    index = 0
    count = 0
    seen = {}
    k = 0
    while k < n1:
        for c in a:
            if c == b[index]:
                index += 1
                if index == len(b):
                    index = 0
                    count += 1
        k += 1
        if index in seen:
            k0, count0 = seen[index]
            cycle = k - k0
            cycles = (n1 - k) // cycle
            count += cycles * (count - count0)
            k += cycles * cycle
            while k < n1:
                for c in a:
                    if c == b[index]:
                        index += 1
                        if index == len(b):
                            index = 0
                            count += 1
                k += 1
            break
        seen[index] = (k, count)
    return count // n2


# ---- test harness ---------------------------------------------------------


def show(s1, n1, s2, n2):
    m = get_max_repetitions(s1, n1, s2, n2)
    print(f'["{s1}", {n1}], ["{s2}", {n2}] -> {m}')


seed = 466


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    show("acb", 4, "ab", 2)
    show("acb", 1, "acb", 1)
    show("abc", 3, "d", 1)
    show("aaa", 3, "aa", 1)
    show("ab", 1000000, "ba", 1)
    show("bacaba", 3, "abacab", 1)
    show("abcd", 1000000, "dcba", 7)
    show("lovelive", 100000, "lovelive", 100000)
    show("baba", 11, "baab", 1)
    show("aabaa", 1000000, "aba", 3)
    count = 300
    total = 0
    checksum = 0
    for _ in range(count):
        letters = 2 + next_random() % 3
        s1 = random_word(1 + next_random() % 8, letters)
        n1 = 1 + next_random() % 1000
        s2 = random_word(1 + next_random() % 4, letters)
        n2 = 1 + next_random() % 5
        m = get_max_repetitions(s1, n1, s2, n2)
        total += m
        checksum = (checksum * 31 + m) % 1000000007
    print(f"{count} random cases: {total} repetitions in all, checksum {checksum}")


main()
