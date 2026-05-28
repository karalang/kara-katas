# LeetCode #13: Roman to Integer — Python mirror of greedy.kara.
# Same algorithm (forward scan + lookahead), same case list, same output.


def value(c: str) -> int:
    if c == 'I': return 1
    if c == 'V': return 5
    if c == 'X': return 10
    if c == 'L': return 50
    if c == 'C': return 100
    if c == 'D': return 500
    if c == 'M': return 1000
    return 0


def roman_to_int(s: str) -> int:
    n = len(s)
    total = 0
    i = 0
    while i < n:
        cur = value(s[i])
        if i + 1 < n:
            nxt = value(s[i + 1])
            if cur < nxt:
                total -= cur
            else:
                total += cur
        else:
            total += cur
        i += 1
    return total


def report(s: str) -> None:
    print(roman_to_int(s))


def main() -> None:
    report("III")
    report("IV")
    report("IX")
    report("LVIII")
    report("MCMXCIV")
    report("I")
    report("XL")
    report("CM")
    report("CDXLIV")
    report("MMXXIV")
    report("MMMDCCCLXXXVIII")
    report("MMMCMXCIX")


if __name__ == "__main__":
    main()
