# LeetCode #1017: Convert to Base -2 -- division by -2
# Mirrors negabase.kara; its output is byte-identical.


def base_neg2(n):
    if n == 0:
        return "0"
    rest = n
    digits = []
    while rest != 0:
        bit = rest & 1
        digits.append("1" if bit == 1 else "0")
        # rest - bit is a multiple of -2, so this division is exact
        rest = (rest - bit) // -2
    return "".join(reversed(digits))


seed = 1017


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def fold(check, digits):
    c = check
    for ch in digits:
        c = (c * 3 + (2 if ch == "1" else 1)) % 1000000007
    return (c * 3) % 1000000007


def main():
    examples = [2, 3, 4, 0, 1, 5, 6, 7, 10, 21, 42, 100, 1365, 1366, 1000000, 999999999, 1000000000]
    for n in examples:
        print(f"n = {n} -> {base_neg2(n)}")
    for rnd in range(2):
        count = 20001 if rnd == 0 else 2000
        digits = ones = longest = check = 0
        for i in range(count):
            if rnd == 0:
                n = i
            else:
                hi = next_random()
                n = (hi * 32768 + next_random()) % 1000000001
            form = base_neg2(n)
            digits += len(form)
            ones += form.count("1")
            longest = max(longest, len(form))
            check = fold(check, form)
        label = "n = 0..20000" if rnd == 0 else "2000 random n up to 10^9"
        print(f"{label}: {digits} digits, {ones} ones, longest {longest}, checksum {check}")


main()
