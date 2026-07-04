"""LeetCode #58: Length of Last Word — reverse scan, O(n) time, O(1) space.

Mirror of length_of_last_word.kara: same skip-trailing-spaces then
count-the-run reverse scan, same output format (`"<input>: <len>"` per line)
so the two files diff line-for-line. Indexes characters directly; the .kara
mirror uses a byte view because the ASCII input makes byte index == char
index.
"""


def length_of_last_word(s: str) -> int:
    i = len(s) - 1

    # Skip trailing spaces.
    while i >= 0 and s[i] == " ":
        i -= 1

    # Count the run of non-space characters ending at i.
    length = 0
    while i >= 0 and s[i] != " ":
        length += 1
        i -= 1
    return length


def report(s: str) -> None:
    print(f"{s}: {length_of_last_word(s)}")


def main() -> None:
    report("Hello World")                  # 5
    report("   fly me   to   the moon  ")  # 4
    report("luffy is still joyboy")        # 6
    report("word")                         # 4
    report("a")                            # 1
    report("   lead")                      # 4
    report("day ")                         # 3
    report("a   bb   ccc   ")              # 3
    report("hello a")                      # 1


if __name__ == "__main__":
    main()
