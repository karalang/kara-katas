# LeetCode #953: Verifying an Alien Dictionary -- a rank per letter.
#
# Number the letters by their place in the order, then compare each word
# with the next: at the first place they differ, the earlier word's
# letter must rank lower, and when one word runs out first it must be the
# earlier one. Sorted pairs side by side make a sorted list, since the
# order on words is transitive. O(total letters).


def is_alien_sorted(words, order):
    rank = [0] * 26
    for i in range(26):
        rank[ord(order[i]) - 97] = i
    for w in range(1, len(words)):
        a = words[w - 1]
        b = words[w]
        k = 0
        while k < len(a) and k < len(b) and a[k] == b[k]:
            k += 1
        if k == len(b):
            if k < len(a):
                return False
        elif k < len(a) and rank[ord(a[k]) - 97] > rank[ord(b[k]) - 97]:
            return False
    return True


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


# The 26 letters in a random order.
def random_order():
    letters = [chr(97 + i) for i in range(26)]
    for i in range(26):
        j = i + next_random() % (26 - i)
        letters[i], letters[j] = letters[j], letters[i]
    return "".join(letters)


# n words of 1 to length letters, each from the first `letters` of `order`.
def random_words(n, length, letters, order):
    words = []
    for _ in range(n):
        m = 1 + next_random() % length
        s = ""
        for _ in range(m):
            s += order[next_random() % letters]
        words.append(s)
    return words


# The words sorted by the alien order.
def alien_sorted(words, order):
    rank = {c: i for i, c in enumerate(order)}
    return sorted(words, key=lambda w: [rank[c] for c in w])


def show(words):
    return "[" + ",".join(words) + "]"


def b(x):
    return "true" if x else "false"


def main():
    global seed
    english = "abcdefghijklmnopqrstuvwxyz"
    # LeetCode's three examples, then a few more
    cases = [
        (["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz"),
        (["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"),
        (["apple", "app"], english),
        (["a"], english),
        (["app", "apple"], english),
        (["kuvp", "q"], "ngxlkthsjuoqcpavbfdermiywz"),
        (["ab", "ab"], english),
        (["ba", "ab"], "bacdefghijklmnopqrstuvwxyz"),
        (["z", "x", "z"], english),
    ]
    for words, order in cases:
        print(f"{show(words)} in {order}: {b(is_alien_sorted(words, order))}")
    # 300 random cases of 1 to 10 words of 1 to 5 letters, from 1 to 4
    # letters of a random order, every second one sorted first
    seed = 953
    count = 0
    sorted_ = 0
    check = 0
    for c in range(300):
        order = random_order()
        n = 1 + next_random() % 10
        letters = 1 + next_random() % 4
        words = random_words(n, 5, letters, order)
        if c % 2 == 0:
            words = alien_sorted(words, order)
        ok = is_alien_sorted(words, order)
        count += n
        if ok:
            sorted_ += 1
        check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"300 random cases of {count} words: {sorted_} sorted, checksum {check}")
    # LeetCode's largest: 100 words of up to 20 letters
    order = random_order()
    words = alien_sorted(random_words(100, 20, 26, order), order)
    print(f"100 words, sorted: {b(is_alien_sorted(words, order))}")
    swapped = list(words)
    swapped[49], swapped[50] = swapped[50], swapped[49]
    print(f"100 words, two in the middle swapped: {b(is_alien_sorted(swapped, order))}")
    reversed_ = [words[99 - i] for i in range(100)]
    print(f"100 words, reversed: {b(is_alien_sorted(reversed_, order))}")
    same = []
    chain = []
    s = ""
    for i in range(100):
        same.append(words[0])
        if i < 20:
            s += "q"
        chain.append(s)
    print(f"100 copies of one word: {b(is_alien_sorted(same, order))}")
    print(f"q to 20 q's, then 80 more of them: {b(is_alien_sorted(chain, order))}")
    back = [chain[99 - i] for i in range(100)]
    print(f"the same, longest first: {b(is_alien_sorted(back, order))}")


main()
