"""LeetCode 140 — Word Break II (Python mirror / oracle).

Backtracking: solve(start) returns all sentences for the suffix s[start:].
At start == n the only sentence is empty; otherwise for each dictionary word
matching s[start:end], prepend it to every sentence of the remaining suffix.
Output sorted for a deterministic mirror.
"""


def solve(s, start, n, dict_):
    out = []
    if start == n:
        out.append("")
        return out
    for end in range(start + 1, n + 1):
        word = s[start:end]
        if word in dict_:
            for tail in solve(s, end, n, dict_):
                if len(tail) == 0:
                    out.append(word)
                else:
                    out.append(word + " " + tail)
    return out


def word_break(s, dict_):
    return sorted(solve(s, 0, len(s), dict_))


def emit(s, dict_):
    res = word_break(s, dict_)
    print(len(res))
    for r in res:
        print(r)


def main():
    emit("catsanddog", {"cat", "cats", "and", "sand", "dog"})
    emit("pineapplepenapple", {"apple", "pen", "applepen", "pine", "pineapple"})
    emit("catsandog", {"cats", "dog", "sand", "and", "cat"})


main()
