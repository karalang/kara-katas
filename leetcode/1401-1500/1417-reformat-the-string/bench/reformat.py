# LeetCode #1417 bench, Python: the letters and the digits apart, each in
# its order, woven together from the larger group, workload and checksum as
# reformat.kara.


def reformat(s):
    letters = [c for c in s if c.islower()]
    digits = [c for c in s if c.isdigit()]
    if abs(len(letters) - len(digits)) > 1:
        return ""
    first, second = (digits, letters) if len(digits) > len(letters) else (letters, digits)
    out = []
    for i in range(len(first)):
        out.append(first[i])
        if i < len(second):
            out.append(second[i])
    return "".join(out)


def main():
    seed = 1417
    parts = []
    for _ in range(100000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        r = seed // 65536
        letter = "abcxyz"[r % 6]
        digit = str(r // 6 % 10)
        parts.append(letter + digit if r // 60 % 2 == 0 else digit + letter)
    pool = "".join(parts)
    check = 0
    for _ in range(20000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        start = 2 * (seed // 65536 % 99750)
        out = reformat(pool[start:start + 500])
        total = 0
        for b in out.encode():
            total = (total * 31 + b) % 1000000007
        check = (check * 131 + total) % 1000000007
    print(f"20000 windows of 500 characters: checksum {check}")


main()
