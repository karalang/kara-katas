# LeetCode #709: To Lower Case -- character by character.
# Benchmark mirror of the Kara star arm: copy each character into a new
# string, moving 'A' to 'Z' up by 32.


def to_lower_case(s):
    out = []
    for c in s:
        if "A" <= c <= "Z":
            out.append(chr(ord(c) + 32))
        else:
            out.append(c)
    return "".join(out)


def main():
    seed = 709

    def next_random():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return seed // 65536

    strings = []
    for _ in range(10000):
        strings.append("".join(chr(32 + next_random() % 95) for _ in range(100)))
    results = list(strings)
    total = 0
    for rnd in range(50):
        for i in range(10000):
            results[i] = to_lower_case(strings[i])
            total += ord(results[i][(rnd + i) % 100])
    for t in results:
        total += sum(t.encode())
    print(f"50 rounds of 10000 strings of 100 characters: sum {total}")


main()
