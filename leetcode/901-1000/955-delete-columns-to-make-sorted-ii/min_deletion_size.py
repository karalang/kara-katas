# LeetCode #955: Delete Columns to Make Sorted II -- pairs settled.
#
# Take the columns left to right, keeping each one unless it puts some
# pair of neighbouring strings out of order. A pair is settled once a
# kept column has the upper string's letter smaller; until then the kept
# columns are equal on it, so the next column decides. A column that
# breaks an unsettled pair must go, since every kept column before it
# is equal there; keeping every column that can stay only settles more
# pairs. O(n m) for n strings of length m.


def min_deletion_size(strs):
    n = len(strs)
    m = len(strs[0])
    settled = [False] * n
    deleted = 0
    for c in range(m):
        breaks = False
        for i in range(n - 1):
            if not settled[i] and strs[i][c] > strs[i + 1][c]:
                breaks = True
                break
        if breaks:
            deleted += 1
            continue
        for i in range(n - 1):
            if strs[i][c] < strs[i + 1][c]:
                settled[i] = True
    return deleted


# ---- test harness ---------------------------------------------------------

def next_random(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def random_strs(seed, n, m, letters):
    out = []
    for _ in range(n):
        out.append("".join(chr(97 + next_random(seed) % letters) for _ in range(m)))
    return out


def show(strs):
    return "[" + ",".join(strs) + "]"


def main():
    cases = [
        ["ca", "bb", "ac"],
        ["xc", "yb", "za"],
        ["zyx", "wvu", "tsr"],
        ["a"],
        ["ab", "aa"],
        ["aa", "aa"],
        ["xga", "xfb", "yfa"],
        ["abx", "agz", "bgc", "bfc"],
        ["ba", "ab", "ab"],
    ]
    for strs in cases:
        print(f"{show(strs)}: {min_deletion_size(list(strs))}")
    seed = [955]
    count = 0
    total = 0
    check = 0
    for _ in range(300):
        n = 1 + next_random(seed) % 8
        m = 1 + next_random(seed) % 6
        strs = random_strs(seed, n, m, 3)
        d = min_deletion_size(strs)
        count += n
        total += d
        check = (check * 31 + d) % 1000000007
    print(f"300 random cases of {count} strings: {total} columns deleted, checksum {check}")
    wide = random_strs(seed, 100, 100, 26)
    print(f"100 random strings of 100 letters: {min_deletion_size(list(wide))}")
    srt = sorted(wide)
    print(f"the same sorted: {min_deletion_size(list(srt))}")
    print(f"the same sorted backwards: {min_deletion_size(srt[::-1])}")
    narrow = random_strs(seed, 100, 100, 2)
    print(f"100 random strings of 100 letters from a and b: {min_deletion_size(list(narrow))}")
    by_prefix = sorted(narrow, key=lambda s: s[:9])
    print(f"the same sorted by their first 9 letters only: {min_deletion_size(by_prefix)}")
    print(f"100 copies of one string: {min_deletion_size([wide[0]] * 100)}")
    last = []
    for i in range(100):
        last.append(wide[0][:-1] + chr(ord('z') - i % 26))
    print(f"one string with a falling last letter: {min_deletion_size(last)}")


main()
