# Reference oracle for the bespoke utf8-codepoints kata.
#
# Emits, per input, the SAME line the Kara programs emit:
#
#   "<s>" B<bytes> C<codepoints> | <scalar> <scalar> ... | L<letters> N<numbers> O<other>
#
# The dual oracle (an external, known-correct answer -- not "interp == codegen
# agree") is Python's own UTF-8 view of each string:
#   * codepoint count   = len(s)        (vs the UTF-8 byte length len(s.encode))
#   * each scalar value = ord(c)        (== the manually decoded cp)
#   * classification    = str.isalpha() / str.isnumeric()
#
# The corpus is defined as explicit Unicode scalar lists (NOT source-level
# glyphs or escapes) so the byte sequence is editor-, terminal-, and
# normalization-proof and provably identical, codepoint for codepoint, to the
# Kara files, which build the same strings from the same integers.
CORPUS = [
    [],                                                        # empty
    [104, 101, 108, 108, 111],                                 # "hello" (ASCII, 1-byte)
    [104, 0xe9, 108, 108, 111],                                # "h<e-acute>llo" (2-byte)
    [0x3a9, 0x3bc, 0x3ad, 0x3b3, 0x3b1],                       # Greek (2-byte each)
    [0x41f, 0x440, 0x438, 0x432, 0x435, 0x442],               # Cyrillic "Privet" (2-byte)
    [0x65e5, 0x672c, 0x8a9e],                                  # CJK "Nihongo" (3-byte each)
    [99, 97, 102, 0xe9, 0x2615],                               # "cafe" + hot-beverage ("other")
    [0x1d11e, 0x1f3b5],                                        # two 4-byte symbols ("other")
    [97, 98, 99, 49, 50, 51, 0x3bb, 0x4e2d, 57, 0x1d11e],     # mixed: all four byte-lengths
    [65, 0xb7, 66],                                            # "A" middle-dot "B" ("other")
    [0x7f, 0x80, 0x7ff, 0x800, 0xffff, 0x10000, 0x10ffff],    # UTF-8 length boundaries
]


def report(cps):
    s = "".join(chr(c) for c in cps)
    b = len(s.encode("utf-8"))
    letters = sum(1 for c in s if c.isalpha())
    numbers = sum(1 for c in s if (not c.isalpha()) and c.isnumeric())
    other = len(s) - letters - numbers
    vals = " ".join(str(ord(c)) for c in s)
    return f'"{s}" B{b} C{len(s)} | {vals} | L{letters} N{numbers} O{other}'


for cps in CORPUS:
    print(report(cps))
