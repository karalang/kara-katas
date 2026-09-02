"""LeetCode 301 - Remove Invalid Parentheses.

Mirror of remove_invalid_parentheses.kara: same bounded DFS, same one-pass
removal budget, same Set-based dedup, same bytewise sort of the results.

The sort is hand-written rather than `sorted()` for the same reason the Kara
version sorts at all: the answer set arrives in hash order, which differs on
every run of every backend, so the arms can only be compared as sequences once
they are put in a defined order. Python's `sorted()` on `str` compares by code
point, which for this alphabet is the same as bytewise - but spelling the
comparison out keeps the five mirrors provably identical rather than
coincidentally so.
"""


def str_less(a: str, b: str) -> bool:
    ab, bb = a.encode(), b.encode()
    n = min(len(ab), len(bb))
    for i in range(n):
        if ab[i] != bb[i]:
            return ab[i] < bb[i]
    return len(ab) < len(bb)


def sort_strings(items: list[str]) -> None:
    for i in range(1, len(items)):
        j = i
        while j > 0 and str_less(items[j], items[j - 1]):
            items[j], items[j - 1] = items[j - 1], items[j]
            j -= 1


def removal_budget(s: str) -> tuple[int, int]:
    """The unmatchable '(' and ')' counts - the minimum removals, in one pass."""
    lrem = rrem = 0
    for c in s:
        if c == "(":
            lrem += 1
        elif c == ")":
            if lrem > 0:
                lrem -= 1
            else:
                rrem += 1
    return lrem, rrem


def walk(
    s: str,
    i: int,
    open_count: int,
    lrem: int,
    rrem: int,
    cur: str,
    seen: set[str],
    out: list[str],
) -> None:
    if i == len(s):
        if lrem == 0 and rrem == 0 and open_count == 0 and cur not in seen:
            seen.add(cur)
            out.append(cur)
        return

    c = s[i]

    # Spend a unit of budget on this character.
    if c == "(" and lrem > 0:
        walk(s, i + 1, open_count, lrem - 1, rrem, cur, seen, out)
    elif c == ")" and rrem > 0:
        walk(s, i + 1, open_count, lrem, rrem - 1, cur, seen, out)

    # Keep it. A ')' may only be kept against an open '('.
    if c == "(":
        walk(s, i + 1, open_count + 1, lrem, rrem, cur + c, seen, out)
    elif c == ")":
        if open_count > 0:
            walk(s, i + 1, open_count - 1, lrem, rrem, cur + c, seen, out)
    else:
        walk(s, i + 1, open_count, lrem, rrem, cur + c, seen, out)


def remove_invalid_parentheses(s: str) -> list[str]:
    lrem, rrem = removal_budget(s)
    seen: set[str] = set()
    out: list[str] = []
    walk(s, 0, 0, lrem, rrem, "", seen, out)
    sort_strings(out)
    return out


def report(s: str) -> None:
    body = ", ".join(f'"{r}"' for r in remove_invalid_parentheses(s))
    print(f'"{s}" -> [{body}]')


def main() -> None:
    report("()())()")
    report("(a)())()")
    report(")(")
    report("")
    report("(((")
    report("n")
    report("()")
    report("()())()(")
    report("()(()")
    report("(a(b(c)d)")


if __name__ == "__main__":
    main()
