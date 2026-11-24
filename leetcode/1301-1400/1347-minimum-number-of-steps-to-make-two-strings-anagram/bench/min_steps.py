# LeetCode #1347 bench -- Python: one count per letter, up for s and down
# for t, the positive counts summed.


def min_steps(s, t):
    count = [0] * 26
    for ch in s:
        count[ord(ch) - 97] += 1
    for ch in t:
        count[ord(ch) - 97] -= 1
    return sum(c for c in count if c > 0)


def main():
    seed = 1347
    letters = []
    for _ in range(1000000):
        seed = (seed * 1103515245 + 12345) % 2147483648
        letters.append(chr(97 + (seed // 65536) % 26))
    text = "".join(letters)
    check = 0
    for q in range(1000):
        n = 40000 + check % 10001
        a = check % (1000000 - n)
        b = (check // 7) % (1000000 - n)
        steps = min_steps(text[a:a + n], text[b:b + n])
        check = (check * 31 + steps + q) % 1000000007
    print(f"1000 queries over a text of 10^6: checksum {check}")


main()
