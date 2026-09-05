"""LeetCode #319: Bulb Switcher — Python mirror of bulb_switcher.kara.

Same algorithm (Newton's integer square root, no floats anywhere), same demo
cases, byte-identical output."""


def isqrt(n: int) -> int:
    if n < 2:
        return n
    x = n
    while True:
        y = (x + n // x) // 2
        if y >= x:
            break
        x = y
    return x


def bulb_switch(n: int) -> int:
    return isqrt(n)


def main() -> None:
    cases = [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 15, 16, 99, 100, 101,
             999999, 1000000, 1000000000, 4503599761588224]
    for n in cases:
        print(f"n = {n} -> {bulb_switch(n)}")


if __name__ == "__main__":
    main()
