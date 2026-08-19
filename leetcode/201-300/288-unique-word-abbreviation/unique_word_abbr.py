"""LeetCode 288 — Unique Word Abbreviation. Oracle mirror of unique_word_abbr.kara.

Same index as the starred Kara file: an abbreviation maps to the SOLE distinct
word that produces it, or to a conflict marker once two do. `None` (absence)
is the third state. Output must match the Kara version byte for byte.
"""

CONFLICTED = object()


def abbrev(w: str) -> str:
    # A word of two characters or fewer has no middle to shrink.
    return w if len(w) <= 2 else f"{w[0]}{len(w) - 2}{w[-1]}"


def build(dictionary):
    idx = {}
    for w in dictionary:
        a = abbrev(w)
        prev = idx.get(a)
        if prev is None:
            idx[a] = w
        elif prev is not CONFLICTED and prev != w:
            # A DIFFERENT word — a real collision. A repeat of the word already
            # stored is not one, which is what makes ["deer","deer"] unique.
            idx[a] = CONFLICTED
    return idx


def is_unique(idx, word: str) -> bool:
    hit = idx.get(abbrev(word))
    if hit is None:
        return True
    if hit is CONFLICTED:
        return False
    return hit == word


def report(idx, word: str) -> None:
    # Kara prints bools as `true`/`false`.
    print(f"is_unique({word}) = {str(is_unique(idx, word)).lower()}")


def main() -> None:
    idx = build(["deer", "door", "cake", "card"])
    for w in ("dear", "cart", "cane", "make", "cake"):
        report(idx, w)

    pidx = build(["deer", "door"])
    report(pidx, "deer")
    report(pidx, "dear")

    didx = build(["deer", "deer", "deer"])
    report(didx, "deer")
    report(didx, "dear")

    sidx = build(["it", "a", "do"])
    for w in ("it", "is", "a", "hello"):
        report(sidx, w)


if __name__ == "__main__":
    main()
