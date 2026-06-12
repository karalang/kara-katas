# LeetCode #722: Remove Comments — reference oracle.
#
# A C++ source is given as a list of lines. Strip `//` line comments and
# `/* ... */` block comments. The first effective marker wins; a block
# comment can span lines, joining code before `/*` on one line with code
# after the matching `*/` on a later line. A line that is empty after
# stripping is dropped (unless it was joined into a continuing buffer).
#
# LeetCode guarantees the source has no single/double-quote characters, so
# there is no string-literal state to track here (the self-hosted lexer's
# slice B additionally is string-aware; this kata covers the comment DFA +
# multi-line line/column advance, not quote handling).


def remove_comments(source):
    result = []
    buffer = []
    in_block = False
    for line in source:
        i = 0
        n = len(line)
        while i < n:
            if not in_block:
                if i + 1 < n and line[i] == "/" and line[i + 1] == "/":
                    break  # line comment: ignore the rest of this line
                elif i + 1 < n and line[i] == "/" and line[i + 1] == "*":
                    in_block = True
                    i += 2
                else:
                    buffer.append(line[i])
                    i += 1
            else:
                if i + 1 < n and line[i] == "*" and line[i + 1] == "/":
                    in_block = False
                    i += 2
                else:
                    i += 1
        # Flush only when we end the line outside a block comment; while
        # inside one the implicit newline is consumed.
        if not in_block and buffer:
            result.append("".join(buffer))
            buffer = []
    return result


def report(name, source):
    out = remove_comments(source)
    print(f'{name} -> [{", ".join(chr(34) + s + chr(34) for s in out)}]')


def main():
    # LeetCode canonical example 1.
    report("ex1", [
        "/*Test program */", "int main()", "{ ",
        "  // variable declaration ", "int a, b, c;",
        "/* This is a test", "   multiline  ", "   comment for ",
        "   testing */", "a = b + c;", "}",
    ])
    # LeetCode canonical example 2 — block joins across three lines.
    report("ex2", ["a/*comment", "line", "more_comment*/b"])

    # Block opens and closes mid-line, joining the surrounding code.
    report("inline", ["a/*c*/b"])
    # Empty block comment.
    report("empty-block", ["/**/"])
    # Whole line is a line comment -> dropped.
    report("line-only", ["// nothing here"])
    # Line comment after code.
    report("trailing-line", ["int x = 1; // set x"])
    # `*/` outside a block is literal text, not a marker.
    report("stray-close", ["a*/b"])
    # `//` inside a block comment is ignored.
    report("slashes-in-block", ["/* // not a line comment */code"])
    # `/*` inside a line comment is ignored.
    report("open-in-line", ["x // /* still a line comment"])
    # Two block comments on one line.
    report("two-blocks", ["a/*1*/b/*2*/c"])
    # Block spanning a line that is otherwise empty.
    report("span-empty", ["start/*", "", "*/end"])
    # Star and slash that are NOT markers.
    report("lone-symbols", ["a / b * c"])
    # A block that consumes a trailing `//` then real code resumes.
    report("block-then-code", ["pre/*x", "y*/post//tail"])
    # Adjacent markers: open immediately after a close.
    report("adjacent", ["a/*x*//*y*/b"])
    # Nothing at all but blank lines.
    report("blanks", ["", "   ", ""])


if __name__ == "__main__":
    main()
