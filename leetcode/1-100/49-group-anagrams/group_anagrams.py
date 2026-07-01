"""LeetCode #49: Group Anagrams — reference oracle.

Sorted-string key: two words are anagrams iff their sorted forms match, so
``''.join(sorted(w))`` is the group key. A dict maps each key to its group;
Python dicts preserve insertion order, so ``list(groups.values())`` yields the
groups in *first-appearance* order with input order inside each — exactly the
canonical form the Kāra solvers ([sorted_key.kara](sorted_key.kara),
[count_signature.kara](count_signature.kara)) produce via their index-map
grouping. Output format matches the Kāra `report` line-for-line so the three
can be diffed directly under `karac run` and `karac build`.
"""

from __future__ import annotations


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups: dict[str, list[str]] = {}
    for w in words:
        key = "".join(sorted(w))
        groups.setdefault(key, []).append(w)
    return list(groups.values())


def report(words: list[str]) -> None:
    groups = group_anagrams(words)
    print(f"{len(groups)} groups")
    for g in groups:
        print(" ".join(g))
    print("---")


def main() -> None:
    report(["eat", "tea", "tan", "ate", "nat", "bat"])   # expect: 3 groups
    report([""])                                         # expect: 1 group
    report(["a"])                                        # expect: 1 group
    report(["abc", "bca", "cab", "xyz", "zzz"])          # expect: 3 groups


if __name__ == "__main__":
    main()
