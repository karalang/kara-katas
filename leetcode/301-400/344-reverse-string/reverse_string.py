# LeetCode #344: Reverse String — Python mirror of reverse_string.kara (the ★ arm).
#
# Two indices walking toward each other, swapping as they go. A Python list of
# one-code-point strings stands in for Kāra's Vec[char].


def reverse_string(s):
    if len(s) < 2:
        return
    i = 0
    j = len(s) - 1
    while i < j:
        t = s[i]
        s[i] = s[j]
        s[j] = t
        i += 1
        j -= 1


def show(s):
    return "".join(s)


def report(text):
    s = list(text)
    reverse_string(s)
    print(f'"{text}" -> "{show(s)}"')


def main():
    # The examples from the problem statement.
    report("hello")
    report("Hannah")

    # Edge lengths, and characters outside ASCII: each `char` is one code
    # point, so these reverse code point by code point.
    report("")
    report("a")
    report("ab")
    report("racecar")
    report("Kāra")
    report("añb€c🦀d")
    report("tab\there")

    # Reversing twice is the identity, on a long string.
    long = [chr((k * 7919) % 26 + 97) for k in range(100000)]
    original = show(long)
    reverse_string(long)
    first = long[0]
    reverse_string(long)
    restores = "true" if show(long) == original else "false"
    print(f"100000 letters: first after one reverse '{first}', twice restores: {restores}")


main()
