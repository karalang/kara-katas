#!/usr/bin/env python3
"""LeetCode #32 bench — Python (mirror of longest_valid_parentheses.kara).

The index-stack longest-valid-parens, stack allocated fresh per call; sliding
window over a fixed pseudo-random parens buffer, folded to a checksum. Same sink
as every other mirror.
"""


def longest_valid_window(buf, start, w):
    stack = [-1]
    best = 0
    for i in range(w):
        if buf[start + i] == 0x28:  # '('
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                top = stack[-1]
                length = i - top
                if length > best:
                    best = length
    return best


def main():
    big_l = 4096
    w = 2048
    total = 330000
    modulus = 1000000007

    buf = bytearray()
    x = 0x12345
    for _ in range(big_l):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        buf.append(0x28 if (x & 1) == 0 else 0x29)  # '(' : ')'

    span = big_l - w + 1
    acc = 0
    for k in range(total):
        start = (k * 7) % span
        r = longest_valid_window(buf, start, w)
        acc = (acc + r) % modulus

    print(acc)


if __name__ == "__main__":
    main()
