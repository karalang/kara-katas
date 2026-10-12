# LeetCode #388: Longest Absolute File Path -- path lengths by depth.
# Mirrors length_longest_path.kara.


def length_longest_path(s):
    length = [0]
    best = 0
    i = 0
    while i < len(s):
        depth = 0
        while i < len(s) and s[i] == "\t":
            depth += 1
            i += 1
        start = i
        is_file = False
        while i < len(s) and s[i] != "\n":
            if s[i] == ".":
                is_file = True
            i += 1
        path = length[depth] + (i - start)
        if is_file:
            best = max(best, path)
        elif depth + 1 < len(length):
            length[depth + 1] = path + 1
        else:
            length.append(path + 1)
        i += 1
    return best


def show(label, s):
    print(f"{label}: {length_longest_path(s)}")


def step(seed):
    seed[0] = (seed[0] * 1103515245 + 12345) % 2147483648
    return seed[0] // 65536


def listing(seed, entries):
    out = []
    open_ = 0
    depth = 0
    for k in range(entries):
        r = step(seed) % 100
        if r < 35:
            depth = open_
        elif r >= 70:
            up = (r - 70) // 10 + 1
            depth = 0 if up > depth else depth - up
        if depth > open_:
            depth = open_
        name_len = step(seed) % 12 + 1
        is_file = step(seed) % 3 == 0
        if k > 0:
            out.append("\n")
        out.append("\t" * depth)
        for _ in range(name_len):
            out.append(chr(step(seed) % 26 + 97))
        if is_file:
            out.append(".ext")
            open_ = depth
        else:
            open_ = depth + 1 if depth < 6 else depth
    return "".join(out)


def main():
    show("example 1", "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext")
    show("example 2", "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext")
    show("no files", "a")
    show("one file at the root", "file.txt")
    show("three files at the root", "file1.txt\nfile2.txt\nlongfile.txt")
    show("a name with a dot is a file", "dir\n\ta.b\n\tsub\n\t\tc")
    show("deep file loses to a long shallow one", "d\n\te\n\t\tf\n\t\t\tg.h\nverylongname.txt")
    show("empty directories", "a\n\tb\n\t\tc\nd")
    show("file after a deep dir", "a\n\tb\n\t\tc\n\t\t\td\nx.y")
    show("names with spaces", "dir\n\t a b.txt\n\tsub dir \n\t\t c");
    seed = [388]
    checksum = longest = none = 0
    for _ in range(2000):
        entries = step(seed) % 30 + 1
        r = length_longest_path(listing(seed, entries))
        if r == 0:
            none += 1
        longest = max(longest, r)
        checksum = (checksum * 31 + r) % 1000000007
    print(f"2000 random listings: longest {longest}, {none} without files, checksum {checksum}")


main()
