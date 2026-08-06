"""LeetCode #249: Group Shifted Strings — oracle for the Kara solvers.

Mirrors `group_shifted.kara`'s canonical-form key (shift every character down
so the first becomes 'a') and its determinism rules: groups in first-seen key
order, words within a group in input order. LeetCode accepts any order; a
cross-language differential does not.
"""


def canonical(word):
    if not word:
        return ""
    shift = ord(word[0]) - ord('a')
    return "".join(f"{(ord(c) - ord('a') - shift) % 26}," for c in word)


def group_shifted(words):
    table, order = {}, []
    for w in words:
        k = canonical(w)
        if k not in table:
            table[k] = []
            order.append(k)
        table[k].append(w)
    return [table[k] for k in order]


def show(groups):
    for g in groups:
        print("[" + ",".join(g) + "]")


if __name__ == "__main__":
    show(group_shifted(["abc", "bcd", "acef", "xyz", "az", "ba", "a", "z"]))
    print("--")
    show(group_shifted(["a"]))
    print("--")
    show(group_shifted(["az", "ba", "bc", "cd", "zy"]))
