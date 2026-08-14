#!/usr/bin/env python3
"""LeetCode 273 — Integer to English Words. Mirror of the ★ solver.

Same three-digit chunking, same right-to-left prepend join, same empty string
for a zero group.
"""

SMALL = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
         "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen",
         "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy",
        "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion"]


def group_name(n):
    if n == 0:
        return ""
    if n < 20:
        return SMALL[n]
    if n < 100:
        t = TENS[n // 10]
        r = n % 10
        return t if r == 0 else t + " " + SMALL[r]
    h = SMALL[n // 100] + " Hundred"
    r = group_name(n % 100)
    return h if r == "" else h + " " + r


def number_to_words(n):
    if n == 0:
        return "Zero"
    out = ""
    rem = n
    scale = 0
    while rem > 0:
        part = rem % 1000
        if part > 0:
            piece = group_name(part)
            if scale > 0:
                piece = piece + " " + SCALES[scale]
            out = piece if out == "" else piece + " " + out
        rem //= 1000
        scale += 1
    return out


def main():
    cases = [0, 5, 13, 20, 21, 100, 101, 110, 123, 1000, 1000000, 1000010,
             12345, 1234567, 1000000000, 2147483647]
    for c in cases:
        print(f"{c} -> {number_to_words(c)}")


main()
