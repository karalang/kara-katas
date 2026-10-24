# LeetCode #953: Verifying an Alien Dictionary -- Python mirror of the
# Kara bench program (a rank per letter).


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


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def before(x, y, rank):
    k = 0
    while k < len(x) and k < len(y) and x[k] == y[k]:
        k += 1
    if k == len(y):
        return False
    if k == len(x):
        return True
    return rank[ord(x[k]) - 97] < rank[ord(y[k]) - 97]


def main():
    rounds, count, n = 2000, 200, 100
    seed = [953]
    orders = []
    sets = []
    for s in range(count):
        letters = [chr(97 + i) for i in range(26)]
        for i in range(26):
            j = i + next_random(seed) % (26 - i)
            letters[i], letters[j] = letters[j], letters[i]
        rank = [0] * 26
        for i in range(26):
            rank[ord(letters[i]) - 97] = i
        order = "".join(letters)
        words = []
        for _ in range(n):
            m = 1 + next_random(seed) % 20
            words.append("".join(letters[next_random(seed) % 3] for _ in range(m)))
        for i in range(1, n):
            j = i
            while j > 0 and before(words[j], words[j - 1], rank):
                words[j], words[j - 1] = words[j - 1], words[j]
                j -= 1
        if s % 3 == 2:
            words[n - 2], words[n - 1] = words[n - 1], words[n - 2]
        orders.append(order)
        sets.append(words)
    sorted_count = 0
    check = 0
    for r in range(rounds):
        for i in range(count):
            k = (r + i) % count
            ok = is_alien_sorted(sets[k], orders[k])
            if ok:
                sorted_count += 1
            check = (check * 31 + (1 if ok else 2)) % 1000000007
    print(f"{rounds} rounds over {count} sets of {n} words: {sorted_count} sorted, checksum {check}")


main()
