# LeetCode #2124: Check if All A's Appears Before All B's -- the mirror of
# abba.kara: the answer is that "ba" does not occur.


def check_string(s):
    return "ba" not in s


def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def show(b):
    return "true" if b else "false"


def main():
    for s in ["aaabbb", "abab", "bbb", "a", "b", "ba", "ab"]:
        print(f"{s} -> {show(check_string(s))}")
    seed = [2124]
    ordered = 0
    check = 0
    for rnd in range(5000):
        n = next_random(seed) % 20 + 1
        s = []
        if rnd % 2 == 0:
            for _ in range(n):
                s.append("a" if next_random(seed) % 2 == 0 else "b")
        else:
            split = next_random(seed) % (n + 1)
            swap = next_random(seed) % (n + 1)
            for i in range(n):
                c = "a" if i < split else "b"
                if i + 1 == split and swap == split:
                    c = "b"
                elif i == split and swap == split:
                    c = "a"
                s.append(c)
        if check_string("".join(s)):
            ordered += 1
            check = (check * 31 + n) % 1000000007
    print(f"5000 strings: {ordered} in order, checksum {check}")
    long = "a" * 50 + "b" * 50
    swapped = "a" * 49 + "ba" + "b" * 49
    print(f"100 letters: {show(check_string(long))}, middle swapped: {show(check_string(swapped))}")


main()
