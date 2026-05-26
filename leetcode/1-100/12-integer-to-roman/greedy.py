# LeetCode #12: Integer to Roman — Python mirror of greedy.kara.
# Same algorithm, same case list, same per-line output shape.


def int_to_roman(num: int) -> list[str]:
    out: list[str] = []
    n = num

    while n >= 1000: out.append('M'); n -= 1000
    if    n >= 900:  out.append('C'); out.append('M'); n -= 900
    if    n >= 500:  out.append('D'); n -= 500
    if    n >= 400:  out.append('C'); out.append('D'); n -= 400
    while n >= 100:  out.append('C'); n -= 100
    if    n >= 90:   out.append('X'); out.append('C'); n -= 90
    if    n >= 50:   out.append('L'); n -= 50
    if    n >= 40:   out.append('X'); out.append('L'); n -= 40
    while n >= 10:   out.append('X'); n -= 10
    if    n >= 9:    out.append('I'); out.append('X'); n -= 9
    if    n >= 5:    out.append('V'); n -= 5
    if    n >= 4:    out.append('I'); out.append('V'); n -= 4
    while n >= 1:    out.append('I'); n -= 1

    return out


def report(n: int) -> None:
    print(''.join(int_to_roman(n)))


def main() -> None:
    report(3)
    report(4)
    report(9)
    report(58)
    report(1994)
    report(1)
    report(40)
    report(900)
    report(444)
    report(2024)
    report(3888)
    report(3999)


if __name__ == "__main__":
    main()
