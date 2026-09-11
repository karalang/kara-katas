"""LeetCode #320: Generalized Abbreviation — Python mirror of
generalized_abbreviation.kara.

Same algorithm (walk 0..2^n and run-length encode each mask), same demo cases,
byte-identical output."""


def abbreviations(word: str) -> list[str]:
    n = len(word)
    out = []
    for mask in range(1 << n):
        abbr = []
        run = 0
        for i in range(n):
            if mask & (1 << i):
                run += 1
            else:
                if run > 0:
                    abbr.append(str(run))
                    run = 0
                abbr.append(word[i])
        if run > 0:
            abbr.append(str(run))
        out.append("".join(abbr))
    return out


def report(word: str) -> None:
    all_ = abbreviations(word)
    print(f'"{word}" -> {len(all_)}')
    print(" ".join(all_))


def main() -> None:
    for w in ["word", "", "a", "ab", "abc", "aaaa", "leet"]:
        report(w)

    for w in ["abcdefgh", "mississippi", "abcdefghijklmnop"]:
        all_ = abbreviations(w)
        acc = 0
        chars = 0
        for entry in all_:
            chars += len(entry)
            for ch in entry.encode():
                acc = (acc * 131 + ch) % 1000000007
            acc = (acc * 131 + 7) % 1000000007
        print(f'"{w}" -> {len(all_)} abbreviations, {chars} chars, fold {acc}')


if __name__ == "__main__":
    main()
