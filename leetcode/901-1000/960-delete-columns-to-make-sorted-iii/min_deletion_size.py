# LeetCode #960: Delete Columns to Make Sorted III -- longest chain.
#
# Mirrors min_deletion_size.kara: column k may come before a later column
# j when every string's letter in k is at most its letter in j; keep the
# longest chain of columns under that order and delete the rest.


def min_deletion_size(strs):
    n = len(strs)
    m = len(strs[0])
    longest = [1] * m
    best = 0
    for j in range(m):
        for k in range(j):
            if all(strs[i][k] <= strs[i][j] for i in range(n)):
                longest[j] = max(longest[j], longest[k] + 1)
        best = max(best, longest[j])
    return m - best


# ---- test harness ---------------------------------------------------------

seed = 0


def next_random():
    global seed
    seed = (seed * 1103515245 + 12345) % 2147483648
    return seed // 65536


def random_strs(n, m, letters):
    return ["".join(chr(ord("a") + next_random() % letters) for _ in range(m)) for _ in range(n)]


def show(strs):
    return "[" + ",".join(strs) + "]"


def main():
    global seed
    cases = [
        ["babca", "bbazb"],
        ["edcba"],
        ["ghi", "def", "abc"],
        ["a"],
        ["ba"],
        ["ab", "ba"],
        ["aaa", "aaa"],
        ["acb", "bca", "abc"],
        ["zabcd", "abcde"],
        ["abcdz", "bcdea"],
    ]
    for strs in cases:
        print(f"{show(strs)}: {min_deletion_size(strs)}")
    seed = 960
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random() % 8
        m = 1 + next_random() % 10
        strs = random_strs(n, m, 4)
        d = min_deletion_size(strs)
        count += n
        total += d
        check = (check * 31 + d) % 1000000007
    print(f"300 random cases of {count} strings: {total} columns deleted, checksum {check}")
    wide = random_strs(100, 100, 26)
    print(f"100 random strings of 100 letters: {min_deletion_size(wide)}")
    one = random_strs(1, 100, 26)
    print(f"one random string of 100 letters: {min_deletion_size(one)}")
    narrow = random_strs(100, 100, 2)
    print(f"100 random strings of 100 letters from a and b: {min_deletion_size(narrow)}")
    same = [wide[0]] * 100
    print(f"100 copies of one string: {min_deletion_size(same)}")
    srt = ["".join(sorted(s)) for s in wide]
    print(f"the same with each string's letters sorted: {min_deletion_size(srt)}")
    zig = ""
    for i in range(100):
        k = i % 50
        c = k if k < 25 else 49 - k
        zig += chr(ord("a") + c)
    print(f"a to z and back, twice: {min_deletion_size([zig])}")


main()
