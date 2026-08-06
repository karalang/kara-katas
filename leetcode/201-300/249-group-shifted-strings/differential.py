"""Python twin of `differential.kara` — same LCG, same draw order, same render.

Both Kara groupings must agree with each other and with this file, line for
line. The generator is reproduced exactly: any divergence in the draw order
would silently compare two different corpora.
"""


def canonical(word):
    if not word:
        return ""
    shift = ord(word[0]) - ord('a')
    return "".join(f"{(ord(c) - ord('a') - shift) % 26}," for c in word)


def gap_key(word):
    return "".join(f"{(ord(word[i]) - ord(word[i - 1])) % 26}," for i in range(1, len(word)))


def group_by(words, keyfn):
    table, order = {}, []
    for w in words:
        k = keyfn(w)
        if k not in table:
            table[k] = []
            order.append(k)
        table[k].append(w)
    return [table[k] for k in order]


def render(groups):
    return "".join("[" + ",".join(g) + "]" for g in groups)


def main():
    cases = 4000
    state = 20260249
    disagree = 0
    hsh = 0
    total_groups = 0
    total_words = 0

    def step(s):
        return (s * 1103515245 + 12345) & 2147483647

    for _ in range(cases):
        state = step(state)
        n_words = ((state // 65536) % 6) + 1
        state = step(state)
        n_seeds = ((state // 65536) % 3) + 1

        seeds = []
        for _s in range(n_seeds):
            state = step(state)
            ln = ((state // 65536) % 4) + 1
            w = ""
            for _k in range(ln):
                state = step(state)
                w += chr(((state // 65536) % 26) + ord('a'))
            seeds.append(w)

        words = []
        for _i in range(n_words):
            state = step(state)
            pick = (state // 65536) % n_seeds
            state = step(state)
            shift = (state // 65536) % 26
            src = seeds[pick]
            words.append("".join(
                chr(((ord(ch) - ord('a') + shift) % 26) + ord('a')) for ch in src
            ))

        a = render(group_by(words, canonical))
        b = render(group_by(words, gap_key))
        if a != b:
            disagree += 1
        total_groups += len(group_by(words, canonical))
        total_words += len(words)
        for ch in a.encode():
            hsh = (hsh * 131 + ch) % 1000000007

    print(f"groupings disagree on {disagree} of {cases} cases")
    print(f"{total_groups} groups over {total_words} words")
    print(hsh)


if __name__ == "__main__":
    main()
