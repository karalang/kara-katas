# Benchmark workload — Roman to Integer (LeetCode #13).
# Python mirror of bench/greedy.kara. K=1M (10× scaled-down vs compiled
# mirrors); the README quotes the projected K=10M time so the comparison
# stays in scale.


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


def value(c: str) -> int:
    if c == 'I': return 1
    if c == 'V': return 5
    if c == 'X': return 10
    if c == 'L': return 50
    if c == 'C': return 100
    if c == 'D': return 500
    if c == 'M': return 1000
    return 0


def roman_to_int(r: list[str]) -> int:
    n = len(r)
    total = 0
    i = 0
    while i < n:
        cur = value(r[i])
        if i + 1 < n:
            nxt = value(r[i + 1])
            if cur < nxt:
                total -= cur
            else:
                total += cur
        else:
            total += cur
        i += 1
    return total


def main() -> None:
    k_iters = 1_000_000
    total_sum = 0
    for k in range(k_iters):
        raw = k * 2654435769 + 305419896
        num = (raw % 3999 + 3999) % 3999 + 1
        r = int_to_roman(num)
        total_sum += roman_to_int(r)
    print(total_sum)


if __name__ == "__main__":
    main()
