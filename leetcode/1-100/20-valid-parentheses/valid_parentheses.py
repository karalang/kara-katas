"""LeetCode #20: Valid Parentheses — single-pass stack of expected closers.

Mirror of valid_parentheses.kara: same stack-of-the-expected-closing-bracket
algorithm (push the closer each opener demands; on a closer it must match
the top of stack; a non-empty stack at the end means unclosed openers), and
the same output format (one `"input" -> true/false` line per case) so the
two files diff line-for-line across all twelve cases.
"""

from __future__ import annotations


def is_valid(s: str) -> bool:
    # The stack holds the closer each open bracket demands, so the closer
    # branch is a single equality against the top of stack.
    closer = {"(": ")", "[": "]", "{": "}"}
    stack: list[str] = []
    for c in s:
        if c in closer:
            # Opener: push the matching closer.
            stack.append(closer[c])
        else:
            # Closer: must match the top of stack. An empty stack here is
            # the "closer with no opener" case.
            if not stack or stack.pop() != c:
                return False
    # A non-empty stack means unclosed openers remain.
    return not stack


def report(s: str) -> None:
    print(f'"{s}" -> {"true" if is_valid(s) else "false"}')


def main() -> None:
    report("()")        # true
    report("()[]{}")    # true
    report("(]")        # false
    report("([)]")      # false
    report("{[]}")      # true
    report("(")         # false
    report(")")         # false
    report("((")        # false
    report("]")         # false
    report("([{}])")    # true
    report("(()")       # false
    report("")          # true


if __name__ == "__main__":
    main()
