"""LeetCode #393: UTF-8 Validation — one-pass scan over a byte buffer,
classifying each leading byte by its high bits and verifying the right
number of `10xxxxxx` continuation bytes follow. O(n) time, O(1) extra.

Algorithmic mirror of validate_utf8.kara. Output format matches
line-for-line (lowercase `true`/`false`) so the two can be diffed directly.
"""

from __future__ import annotations


def lead_len(b: int) -> int:
    # Bytes occupied by the character starting with leading byte `b`, or 0
    # if `b` is not a valid UTF-8 leading byte. Masks isolate the high bits.
    if b & 0x80 == 0x00:
        return 1
    if b & 0xE0 == 0xC0:
        return 2
    if b & 0xF0 == 0xE0:
        return 3
    if b & 0xF8 == 0xF0:
        return 4
    return 0


def is_continuation(b: int) -> bool:
    return b & 0xC0 == 0x80


def validate_utf8(data: list[int]) -> bool:
    n = len(data)
    i = 0
    while i < n:
        need = lead_len(data[i])
        if need == 0:
            return False  # not a valid leading byte
        if i + need > n:
            return False  # continuation bytes run past the buffer end
        for k in range(1, need):
            if not is_continuation(data[i + k]):
                return False
        i += need
    return True


def _b(res: bool) -> str:
    return "true" if res else "false"


def validate_lit(name: str, data: list[int]) -> None:
    print(f"{name} -> {_b(validate_utf8(data))}")


def report_str(s: str) -> None:
    # A real UTF-8 string's bytes must always validate.
    print(f'bytes("{s}") -> {_b(validate_utf8(list(s.encode("utf-8"))))}')


def main() -> None:
    validate_lit("[197,130,1]", [197, 130, 1])
    validate_lit("[235,140,4]", [235, 140, 4])

    validate_lit("empty", [])
    validate_lit("[65]", [65])

    validate_lit("[0xC5,0x82]", [0xC5, 0x82])
    validate_lit("[0xEB,0x8C,0x95]", [0xEB, 0x8C, 0x95])
    validate_lit("[0xF0,0x9F,0x98,0x81]", [0xF0, 0x9F, 0x98, 0x81])

    validate_lit("[0x80]", [0x80])
    validate_lit("[0xC0]", [0xC0])
    validate_lit("[0xE0,0x80]", [0xE0, 0x80])
    validate_lit("[0xFF]", [0xFF])
    validate_lit("[0xC5,0x00]", [0xC5, 0x00])

    report_str("Ascii123")
    report_str("héllo")
    report_str("café ☕")
    report_str("日本語")


if __name__ == "__main__":
    main()
