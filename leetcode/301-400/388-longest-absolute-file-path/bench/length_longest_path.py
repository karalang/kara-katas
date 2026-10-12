# Benchmark for #388: mirror of length_longest_path.kara (path lengths by depth).


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
    seed = [388]
    listings = [listing(seed, 800) for _ in range(200)]
    total = sum(len(s) for s in listings)
    checksum = 0
    for rnd in range(150):
        for s in listings:
            checksum = (checksum * 31 + length_longest_path(s) + rnd) % 1000000007
    print(f"{total} bytes in 200 listings, 150 rounds, checksum {checksum}")


main()
