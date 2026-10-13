# Benchmark for #522: Python mirror of the ★ arm (longest first); see
# find_lus_length.kara.


def is_subsequence(small, big):
    s = list(small)
    i = 0
    for c in big:
        if i < len(s) and s[i] == c:
            i += 1
    return i == len(s)


def find_lus_length(strs):
    order = sorted(range(len(strs)), key=lambda i: -len(strs[i]))
    for i in order:
        uncommon = True
        for j in range(len(strs)):
            if j != i and is_subsequence(strs[i], strs[j]):
                uncommon = False
                break
        if uncommon:
            return len(strs[i])
    return -1


seed = 522


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(n, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(n))


def main():
    # 2,000 random lists of 50 words of 1 to 10 letters from 1 to 3
    # letters, one word in three a copy of an earlier one, made once;
    # then every list solved in each of 100 rounds.
    lists = []
    for _ in range(2000):
        letters = 1 + next_random() % 3
        strs = []
        for k in range(50):
            if k > 0 and next_random() % 3 == 0:
                strs.append(strs[next_random() % k])
            else:
                strs.append(random_word(1 + next_random() % 10, letters))
        lists.append(strs)
    total = 0
    checksum = 0
    for rnd in range(100):
        for l in range(len(lists)):
            answer = find_lus_length(lists[l])
            total += answer
            checksum = (checksum + (rnd + 1) * (l + 1) * (answer + 2)) % 1000000007
    print(f"2000 lists of 50 words, 100 rounds: total {total}, checksum {checksum}")


main()
