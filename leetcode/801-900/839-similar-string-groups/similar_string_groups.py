# LeetCode #839: Similar String Groups -- Python mirror of the ★ arm and its harness.

def similar(a, b):
    diff = 0
    for k in range(len(a)):
        if a[k] != b[k]:
            diff += 1
            if diff > 2:
                return False
    return diff != 1

def find(parent, x):
    v = x
    while parent[v] != v:
        parent[v] = parent[parent[v]]
        v = parent[v]
    return v

def num_similar_groups(strs):
    words = [s.encode() for s in strs]
    n = len(words)
    parent = list(range(n))
    groups = n
    for i in range(n):
        for j in range(i + 1, n):
            a = find(parent, i)
            b = find(parent, j)
            if a != b and similar(words[i], words[j]):
                parent[a] = b
                groups -= 1
    return groups

seed = 0

def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536

def random_word(m, letters):
    return [97 + next_random() % letters for _ in range(m)]

def swapped(w, swaps):
    v = list(w)
    for _ in range(swaps):
        p = next_random() % len(v)
        q = next_random() % len(v)
        v[p], v[q] = v[q], v[p]
    return v

def random_family(n, m, letters, far, jump):
    words = [random_word(m, letters)]
    for _ in range(1, n):
        frm = next_random() % len(words)
        swaps = far if next_random() % jump == 0 else 1
        words.append(swapped(words[frm], swaps))
    return [bytes(w).decode() for w in words]

def show(strs):
    print("[" + ", ".join(strs) + "] -> " + str(num_similar_groups(strs)))

def main():
    global seed
    show(["tars", "rats", "arts", "star"])
    show(["omv", "ovm"])
    show(["a"])
    show(["abc", "abc"])
    show(["ab", "ba"])
    show(["aaaa", "aaaa", "aaaa"])
    show(["abcd", "badc"])
    show(["abcd", "badc", "bacd"])
    show(["abc", "acb", "bac", "bca", "cab", "cba"])
    show(["abc", "bca", "cab"])
    show(["aab", "aba", "baa"])
    show(["abcde", "edcba", "abced", "bacde", "edcab"])
    show(["xy", "xy", "yx", "yx"])
    seed = 839
    for letters, far, jump in [(26, 3, 4), (5, 4, 2), (26, 300, 1)]:
        strs = random_family(300, 300, letters, far, jump)
        print(f"300 words of 300 letters from {letters}, {far} swaps 1 in {jump}: {num_similar_groups(strs)} groups")
    strs = random_family(300, 8, 8, 4, 1)
    print(f"300 words of 8 letters, each 4 swaps from an earlier one: {num_similar_groups(strs)} groups")
    check = 0
    total = 0
    for _ in range(300):
        n = 1 + next_random() % 20
        m = 1 + next_random() % 10
        letters = 1 + next_random() % 6
        far = 2 + next_random() % 4
        jump = 1 + next_random() % 4
        groups = num_similar_groups(random_family(n, m, letters, far, jump))
        total += groups
        check = (check * 31 + groups) % 1000000007
    print(f"300 random cases: {total} groups, checksum {check}")

main()
