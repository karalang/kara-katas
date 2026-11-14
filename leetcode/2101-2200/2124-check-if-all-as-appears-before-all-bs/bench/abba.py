# LeetCode #2124: Check if All A's Appears Before All B's -- the
# benchmark, the same algorithm as abba.kara: the answer is that "ba"
# does not occur.


def check_string(s):
    return "ba" not in s


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def main():
    seed = [2124]
    strings = []
    for _ in range(100000):
        split = next_random(seed) % 101
        letters = ["a" if i < split else "b" for i in range(100)]
        if next_random(seed) % 4 == 0:
            at = next_random(seed) % 100
            letters[at] = "b" if letters[at] == "a" else "a"
        strings.append("".join(letters))
    ordered = 0
    check = 0
    for rnd in range(50):
        k = rnd * 7919 % 100000
        at = rnd * 31 % 100
        letters = list(strings[k])
        letters[at] = "b" if letters[at] == "a" else "a"
        strings[k] = "".join(letters)
        for i in range(len(strings)):
            if check_string(strings[i]):
                ordered += 1
                check = (check * 31 + i) % 1000000007
    print(f"5000000 checks: {ordered} in order, checksum {check}")


main()
