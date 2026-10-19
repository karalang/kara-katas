# LeetCode 792 -- Number of Matching Subsequences: the bench, in Python.
# Mirrors num_matching_subseq.kara: every word waits in the bucket of the
# next letter it needs, and s is walked once.


def num_matching_subseq(s, words):
    waiting = [[] for _ in range(26)]
    for i, word in enumerate(words):
        waiting[ord(word[0]) - 97].append((i, 0))
    count = 0
    for ch in s:
        c = ord(ch) - 97
        moving = waiting[c]
        waiting[c] = []
        for w, matched in moving:
            word = words[w]
            if matched + 1 == len(word):
                count += 1
            else:
                waiting[ord(word[matched + 1]) - 97].append((w, matched + 1))
    return count


seed = 792


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_word(length, letters):
    return "".join(chr(97 + next_random() % letters) for _ in range(length))


def main():
    strings = []
    for _ in range(16):
        letters = 13 + next_random() % 14
        strings.append(random_word(50000, letters))
    lists = []
    for _ in range(64):
        lists.append([random_word(1 + next_random() % 50, 26) for _ in range(5000)])
    rounds = 4000
    total = 0
    check = 0
    for r in range(rounds):
        count = num_matching_subseq(strings[r % 16], lists[(r // 16) % 64])
        total += count
        check = (check * 131 + count + 1) % 1000000007
    print(f"{rounds} rounds of 5000 words: {total} matching, checksum {check}")


main()
