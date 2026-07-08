"""LeetCode #68: Text Justification — greedy line packing + even space spread.

Mirror of text_justification.kara: greedily pack the widest run of words that
fits, then distribute the leftover spaces evenly between them with the extra
going to the left gaps; the last line and any single-word line are left-justified
and right-padded. Same eight cases and the same output shape (each line printed
quoted so trailing spaces show, then a `sums:` fold of per-line positional
checksums) so the files diff line-for-line.
"""

from __future__ import annotations


def full_justify(words: list[str], max_width: int) -> list[str]:
    lines: list[str] = []
    n = len(words)

    i = 0
    while i < n:
        # (1) Greedy pack: words[i:j] is the widest run that fits.
        j = i
        line_chars = 0
        count = 0
        while j < n:
            wl = len(words[j])
            if line_chars + wl + count <= max_width:
                line_chars += wl
                count += 1
                j += 1
            else:
                break

        gaps = count - 1
        total = max_width - line_chars
        is_last = j == n

        # (2) Build the line.
        line = ""
        if is_last or count == 1:
            for g in range(count):
                line += words[i + g]
                if g < count - 1:
                    line += " "
            line += " " * (max_width - len(line))
        else:
            base = total // gaps
            extra = total % gaps
            for g in range(count):
                line += words[i + g]
                if g < gaps:
                    sp = base + (1 if g < extra else 0)
                    line += " " * sp

        lines.append(line)
        i = j

    return lines


def report(words: list[str], mw: int, acc: list[str]) -> None:
    for line in full_justify(words, mw):
        print(f'"{line}"')
        chk = sum((k + 1) * ord(c) for k, c in enumerate(line))
        acc.append(str(chk))


def main() -> None:
    acc: list[str] = []
    report(["This", "is", "an", "example", "of", "text", "justification."], 16, acc)
    report(["What", "must", "be", "acknowledgment", "shall", "be"], 16, acc)
    report(["Science", "is", "what", "we", "understand", "well", "enough", "to",
            "explain", "to", "a", "computer.", "Art", "is", "everything", "else",
            "we", "do"], 20, acc)
    report(["a"], 5, acc)
    report(["hello"], 5, acc)
    report(["hi", "there"], 10, acc)
    report(["Listen", "to", "many,", "speak", "to", "a", "few."], 6, acc)
    report(["ask", "not", "what", "your", "country"], 9, acc)
    print("sums: " + " ".join(acc))


if __name__ == "__main__":
    main()
